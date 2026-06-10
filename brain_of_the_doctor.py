# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq_helper import execute_with_fallback, get_groq_keys

# Setup fallback keys validation
if not get_groq_keys():
    raise ValueError("No Groq API keys found. Set GROQ_API_KEY or GROQ_API_KEYS in .env.")

#Step2: Convert image to required format
def encode_image(image_path):   
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#Step3: Setup Multimodal LLM 
def analyze_image_with_query(query, model, encoded_image):
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
            model=model
        )
        return chat_completion.choices[0].message.content

    return execute_with_fallback(_analyze)

if __name__ == "__main__":
    #image_path="acne.jpg"
    image_path = "acne.jpg" # Example
    query = "Is there something wrong with my face?"
    model = "meta-llama/llama-4-scout-17b-16e-instruct"
    # Try running if file exists
    if os.path.exists(image_path):
        result = analyze_image_with_query(query=query, model=model, encoded_image=encode_image(image_path))
        print(result)
    else:
        print(f"Skipping direct test: {image_path} not found.")
