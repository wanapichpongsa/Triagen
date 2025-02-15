import os
from dotenv import load_dotenv
import requests
import json

# API Configuration
BASE_URL = "https://api.ragie.ai"
INSTRUCTIONS_ENDPOINT = f"{BASE_URL}/instructions"

def create_instructions():
    load_dotenv()
    api_key = os.getenv("RAGIE_API_KEY")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    instruction_data = {
        "name": "Medical Triage Assessment",
        "active": True,
        "scope": "document",
        "prompt": "Analyze the patient's symptoms and medical history for triage assessment.", # Needs to be more specific.
        "entity_schema": {
            "type": "object",
            "properties": {
                "urgency_level": {
                    "type": "string",
                    "enum": ["immediate", "urgent", "non-urgent"] # Let's try follow NHS 10-second triage system if possible.
                },
                "symptoms": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "recommended_action": {
                    "type": "string",
                    "enum": ["emergency", "urgent_care", "primary_care", "self_care"] # # P-3, P-2, P-1?
                }
            },
            "required": ["urgency_level", "symptoms", "recommended_action"]
        }
    }

    response = requests.post(INSTRUCTIONS_ENDPOINT, headers=headers, json=instruction_data)
    print(response.text)

def main():
    create_instructions()

if __name__ == "__main__":
    main()