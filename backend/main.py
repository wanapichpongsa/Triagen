import os
from dotenv import load_dotenv
import requests

def get_instructions():
    load_dotenv()  # Load environment variables

    url = "https://api.ragie.ai/instructions"
    api_key = os.getenv("RAGIE_API_KEY")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.get(url, headers=headers)
    print(response.text)

def main():
    get_instructions()

if __name__ == "__main__":
    main()