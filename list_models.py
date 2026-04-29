import os
import dotenv
import google.generativeai as genai

dotenv.load_dotenv(override=True)
raw_key = os.getenv('PORTAL_NEURAL_LINK_KEY', '')
key = raw_key.strip().strip('"\'')
genai.configure(api_key=key)

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
