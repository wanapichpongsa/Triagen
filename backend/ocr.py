import os
from PIL import Image
from dotenv import load_dotenv

from google import genai
load_dotenv()

def gemini_vision(filename: str, debug: bool = False) -> str:
    try:
        image = Image.open(f"database/data/{filename}")
        if not image:
            raise ValueError("Image not found")
            
        api_key = os.getenv("GEMINI_API")
        if not api_key:
            raise ValueError("GEMINI_API environment variable not set")
            
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Extract the medical form structure and return ONLY a valid JSON object as string, no markdown code blocks or other text.",
                image
            ])
            
        if debug:
            print(f"Raw Gemini response: {response.text}")
            
        # Ensure we got a response and strip ```json``` markers if present
        text = response.text
        if not text:
            raise ValueError("Empty response from Gemini")
        
        # Remove ```json and ``` if present
        text = text.replace("```json", "").replace("```", "").strip()
            
        return text
            
    except Exception as e:
        print(f"Gemini Vision error: {e}")
        raise