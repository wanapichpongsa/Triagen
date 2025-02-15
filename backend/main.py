import os
from dotenv import load_dotenv

from openai import OpenAI
import pdfplumber
import json
import requests
import base64
import re

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
ragie_api_key = os.getenv("RAGIE_API_KEY")

# API Configuration
BASE_URL = "https://api.ragie.ai"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/documents"
RETRIEVALS_ENDPOINT = f"{BASE_URL}/retrievals"


def ragie_get_datastructure() -> list[str]:
    # PROS: Returns in Markdown format
    # CONS: OCR is weaker than OpenAI

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {ragie_api_key}"
    }

    retrieval_data = {
        "query": "What is the structure of this medical document?"
    }

    document_chunks = requests.post(
        RETRIEVALS_ENDPOINT, 
        headers=headers,
        json=retrieval_data
    )
    document_chunks = document_chunks.json()
    
    """ Print each chunk's document_id
    for chunk in document_chunks["scored_chunks"]:
        print(f"Document ID: {chunk['document_id']}")
        print(f"Document Name: {chunk['document_name']}\n")
        print(f"Text: {chunk['text']}\n")
    """
    document_id = "3c270c93-fec7-4663-8d5e-1e8f59ffacad"
    
    # Collect all chunks from the specified document
    ragie_response = [
        chunk["text"] for chunk in document_chunks["scored_chunks"]
        if chunk["document_id"] == document_id
    ]
    for i, text in enumerate(ragie_response):
        print(f"Chunk {i} from document:", text, "\n\n\n\n\n")
    return ragie_response

def openai_get_datastructure(image_path: str) -> dict[str, any]:
    system_prompt = "You are a medical form parser. Extract the form structure and return it as a JSON object."
    import pytesseract
    from PIL import Image

    # Read and encode image
    image = Image.open(image_path)

    # Use OCR to extract text from the image
    extracted_text = pytesseract.image_to_string(image)
    
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Output only the JSON object, nothing else. extracted_text: {extracted_text}"}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def edit_datastructure(data_structure: dict) -> dict:
    # editing GUI
    # tkinter?
    return {"test": "test"}
    

def log_instance_of_document(data_structure: dict) -> None:
    data_structure = json.dumps(data_structure, indent=4)
    
    # Get next file number
    format_dir = "format"
    existing_files = len([f for f in os.listdir(format_dir) if f.endswith('.json')])
    next_num = existing_files + 1
    
    # Write to new file
    filename = f"format/format{next_num}.json"
    with open(filename, "w") as f:
        f.write(data_structure)

def main():
    # TODO: GET HASH FROM CF and if same openai fn not allowed to run
    response: str = openai_get_datastructure("data/bloodtest-form.png")
    json_response = json.loads(response1, indent=4, strict=False) # why strict=False?
    try:
        while True:
            continue_loop = input("Correct format? (y/n/fin)")
            # Match any number of repeated characters
            if re.match(r"^y+e*s*$", continue_loop.lower()):  # yes, yeees, s, sss
                log_instance_of_document(json_response)
                break
            elif re.match(r"^n+o*$", continue_loop.lower()):  # no, nooo, n
                response1 = edit_datastructure(response1)
            elif re.match(r"^f+i*n+i*s*h*$", continue_loop.lower()):  # fin, finish, fiiinish
                log_instance_of_document(response1)
                break
            else:
                print("Invalid input. Please enter 'y/yes', 'n/no', or 'fin/finish'")
    except KeyboardInterrupt: #TODO: Good practice to have here?
        print("Exiting...")

if __name__ == "__main__":
    main()
    from fbc_guidance import fbc_main
    fbc_main()