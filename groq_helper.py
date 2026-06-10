import os
import logging
from groq import Groq

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_groq_keys():
    """
    Retrieves all available Groq API keys from the environment.
    Supports comma-separated GROQ_API_KEYS or a single GROQ_API_KEY.
    """
    keys = []
    
    # 1. Check for comma-separated list of keys
    keys_str = os.environ.get("GROQ_API_KEYS", "")
    if keys_str:
        keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        
    # 2. Check for single key as fallback/default
    single_key = os.environ.get("GROQ_API_KEY", "")
    if single_key and single_key not in keys:
        keys.append(single_key)
        
    return keys

def execute_with_fallback(func, *args, **kwargs):
    """
    Executes a function (which takes a groq client as its first argument)
    with automatic fallback across multiple keys if rate-limited or failed.
    """
    keys = get_groq_keys()
    if not keys:
        raise ValueError("No Groq API keys found. Set GROQ_API_KEY or GROQ_API_KEYS in .env.")
        
    last_exception = None
    for i, key in enumerate(keys):
        try:
            # Mask key for secure logging
            masked_key = f"{key[:8]}...{key[-5:]}" if len(key) > 13 else "invalid_key_length"
            logging.info(f"Attempting Groq API call using key index {i} ({masked_key})")
            
            client = Groq(api_key=key)
            return func(client, *args, **kwargs)
        except Exception as e:
            last_exception = e
            logging.error(f"Error using Groq key index {i}: {e}. Retrying with next key...")
            
    logging.critical("All configured Groq API keys have failed.")
    raise last_exception
