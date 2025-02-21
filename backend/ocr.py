import os
from PIL import Image
from dotenv import load_dotenv

from google import genai
load_dotenv()

def gemini_vision(filename: str, debug: bool = False) -> str:
    image = Image.open(f"database/data/{filename}")
    if not image:
        raise ValueError("Image not found")
    api_key = os.getenv("GEMINI_API")
    if not api_key:
        raise ValueError("GEMINI_API environment variable not set")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Only output a JSON object of the document structure, nothing else", image]) # Have the json object be 'production ready' e.g., typecasting, header: interface kv pair like bloodtest-form.json
    if debug:
        with open(f"database/debug/{filename}_gemini_results.txt", 'w') as f:
            f.write(response.text)
    return response.text