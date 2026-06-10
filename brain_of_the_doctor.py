# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

import os
import base64
import requests
import logging
from groq_helper import execute_with_fallback, get_groq_keys, get_gemini_keys, get_openrouter_keys, get_together_keys, get_hf_keys, get_mistral_keys

# Setup fallback keys validation (Requires at least one supported provider configured)
has_groq = bool(get_groq_keys())
has_gemini = bool(get_gemini_keys())
has_openrouter = bool(get_openrouter_keys())
has_together = bool(get_together_keys())
has_hf = bool(get_hf_keys())
has_mistral = bool(get_mistral_keys())

if not any([has_groq, has_gemini, has_openrouter, has_together, has_hf, has_mistral]):
    raise ValueError("No API keys found. You must set at least one provider key (GROQ, GEMINI, OPENROUTER, TOGETHER, HF, or MISTRAL) in .env.")


#Step2: Convert image to required format
def encode_image(image_path):   
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Gemini multimodal analysis function (supports multiple Gemini API keys and fallback rotation)
def analyze_image_with_gemini(query, model_name, encoded_image):
    keys = get_gemini_keys()
    if not keys:
        raise ValueError("GEMINI_API_KEY/GOOGLE_API_KEY environment variable is not set.")
        
    last_exception = None
    for i, key in enumerate(keys):
        try:
            # Mask key for secure logging
            masked_key = f"{key[:8]}...{key[-5:]}" if len(key) > 13 else "invalid_key_length"
            logging.info(f"Attempting Gemini API call using key index {i} ({masked_key})")
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": query},
                            {
                                "inlineData": {
                                    "mimeType": "image/jpeg",
                                    "data": encoded_image
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            last_exception = e
            logging.error(f"Error using Gemini key index {i}: {e}. Retrying with next key...")
            
    logging.critical("All configured Gemini API keys have failed.")
    raise last_exception

# OpenRouter multimodal analysis function (supports multiple keys fallback)
def analyze_image_with_openrouter(query, model_name, encoded_image):
    keys = get_openrouter_keys()
    if not keys:
        raise ValueError("OPENROUTER_API_KEY/OPENROUTER_API_KEYS environment variable is not set.")
        
    last_exception = None
    for i, key in enumerate(keys):
        try:
            # Mask key for secure logging
            masked_key = f"{key[:8]}...{key[-5:]}" if len(key) > 13 else "invalid_key_length"
            logging.info(f"Attempting OpenRouter API call using key index {i} ({masked_key})")
            
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "HTTP-Referer": "https://medisync-app.com",
                "X-OpenRouter-Title": "Medisync",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            
            text = result["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            last_exception = e
            logging.error(f"Error using OpenRouter key index {i}: {e}. Retrying with next key...")
            
    logging.critical("All configured OpenRouter API keys have failed.")
    raise last_exception

# Together AI multimodal analysis function (supports multiple keys fallback)
def analyze_image_with_together(query, model_name, encoded_image):
    from groq_helper import get_together_keys
    keys = get_together_keys()
    if not keys:
        raise ValueError("TOGETHER_API_KEY/TOGETHER_API_KEYS environment variable is not set.")
        
    last_exception = None
    for i, key in enumerate(keys):
        try:
            masked_key = f"{key[:8]}...{key[-5:]}" if len(key) > 13 else "invalid_key_length"
            logging.info(f"Attempting Together AI call using key index {i} ({masked_key})")
            
            url = "https://api.together.xyz/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            
            text = result["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            last_exception = e
            logging.error(f"Error using Together AI key index {i}: {e}. Retrying with next key...")
            
    logging.critical("All configured Together AI API keys have failed.")
    raise last_exception

# Hugging Face serverless inference function (supports multiple keys fallback)
def analyze_image_with_hf(query, model_name, encoded_image):
    keys = get_hf_keys()
    if not keys:
        raise ValueError("HF_TOKEN/HUGGINGFACE_API_KEY environment variable is not set.")
        
    last_exception = None
    for i, key in enumerate(keys):
        try:
            masked_key = f"{key[:8]}...{key[-5:]}" if len(key) > 13 else "invalid_key_length"
            logging.info(f"Attempting HuggingFace API call using key index {i} ({masked_key})")
            
            # Use the OpenAI compatible router domain directly (resolves everywhere & supports Partner providers)
            url = "https://router.huggingface.co/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=25)
            response.raise_for_status()
            result = response.json()
            
            # The router uses standard OpenAI format structure
            text = result["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            last_exception = e
            logging.error(f"Error using HuggingFace key index {i}: {e}. Retrying with next key...")
            
    logging.critical("All configured HuggingFace API keys have failed.")
    raise last_exception

# Mistral AI multimodal analysis function (supports multiple keys fallback)
def analyze_image_with_mistral(query, model_name, encoded_image):
    keys = get_mistral_keys()
    if not keys:
        raise ValueError("MISTRAL_API_KEY/MISTRAL_API_KEYS environment variable is not set.")
        
    last_exception = None
    for i, key in enumerate(keys):
        try:
            masked_key = f"{key[:8]}...{key[-5:]}" if len(key) > 13 else "invalid_key_length"
            logging.info(f"Attempting Mistral API call using key index {i} ({masked_key})")
            
            url = "https://api.mistral.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": query
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                }
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            
            text = result["choices"][0]["message"]["content"]
            return text
        except Exception as e:
            last_exception = e
            logging.error(f"Error using Mistral key index {i}: {e}. Retrying with next key...")
            
    logging.critical("All configured Mistral API keys have failed.")
    raise last_exception

#Step3: Setup Multimodal LLM (Supports Groq models, Gemini, OpenRouter, GitHub, HuggingFace, and Mistral)
def analyze_image_with_query(query, model, encoded_image):
    # Route Gemini Models
    if model in ["gemini-flash", "gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]:
        gemini_model_name = "gemini-2.5-flash"
        if model == "gemini-2.5-pro":
            gemini_model_name = "gemini-2.5-pro"
        elif model == "gemini-2.0-flash":
            gemini_model_name = "gemini-2.0-flash"
        return analyze_image_with_gemini(query, gemini_model_name, encoded_image)
        
    # Route OpenRouter Models
    elif model.startswith("openrouter-") or model == "openrouter-nemotron":
        or_model_name = "nvidia/nemotron-nano-12b-v2-vl:free"
        return analyze_image_with_openrouter(query, or_model_name, encoded_image)
        
    # Route Together AI Models
    elif model == "together-llama32-vision":
        return analyze_image_with_together(query, "meta-llama/Llama-3.2-11B-Vision-Instruct", encoded_image)
        
    # Route Hugging Face Models
    elif model == "hf-qwen":
        return analyze_image_with_hf(query, "Qwen/Qwen3-VL-8B-Instruct", encoded_image)
        
    # Route Mistral Models
    elif model == "mistral-pixtral":
        return analyze_image_with_mistral(query, "pixtral-12b", encoded_image)
        
    # Route Groq Models
    groq_model = "meta-llama/llama-4-scout-17b-16e-instruct" # Default
    if model == "groq-llama4":
        groq_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        
    def _analyze(client):
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=groq_model
        )
        return chat_completion.choices[0].message.content

    return execute_with_fallback(_analyze)

if __name__ == "__main__":
    image_path = "acne.jpg" # Example
    query = "Is there something wrong with my face?"
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    if os.path.exists(image_path):
        result = analyze_image_with_query(query=query, model=model, encoded_image=encode_image(image_path))
        print(result)
    else:
        print(f"Skipping direct test: {image_path} not found.")
