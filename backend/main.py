import os
from dotenv import load_dotenv

from openai import OpenAI
import pdfplumber
import json
import requests

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

def openai_get_datastructure(file_path: str) -> dict[str, any]:
    # This is basically what I want get_datastructure() to return:
    system_prompt = "return a JSON object that represents the data structure of the document."
    with open(file_path, "r") as file:
        query = file.read()

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
            ]
    )
    print(response.choices[0].message.content)

def hardcoded_datastructure() -> dict[str, any]:
    # This is basically what I want get_datastructure() to return:
    form_data = {
        "Lab": {
            "Lab Number": None,
            "NHS No.": None,
            "Hospital No.": None,
            "Address": None
        },
        "Patient Details": {
            "Surname": None,
            "Forename": None,
            "Sex": None,
            "DOB": None,
            "Fasting": None,
            "NHS/PP": None,
            "Consultant/GP": None,
            "Ward/Surgery": None
        },
        "Clinical Details and Drug Therapy": None,
        "Requestor": {
            "Name & Signature": None,
            "Bleep No.": None
        },
        "Sample": {
            "Date": None,
            "Time": None,
            "Urgent": None,
            "Type": None  # Blood, Urine, CSF
        },
        "Tests Requested": {
            "Biochemistry": {
                "Brown Top Gel Tube": {
                    "UE": False,
                    "Bone": False,
                    "Liver": False,
                    "Amylase": False,
                    "CRP": False,
                    "Lipids": False,
                    "Thyroid": False,
                    "Glucose Fasting/Random (Yellow Top)": False,
                    "HBA1c (Red Top)": False,
                    "Gent": False,
                    "Digoxin": False,
                    "B12/Folate": False,
                    "Ferritin": False,
                    "Cortisol 9am/Random": False,
                    "Immunoglobulins": False,
                    "Electrophoresis": False
                }
            },
            "Haematology": {
                "Red Top EDTA": {
                    "FBC": False,
                    "ESR": False,
                    "IM": False
                },
                "Green Top Citrate": {
                    "Clotting Screen": False,
                    "INR": False,
                    "D Dimer": False,
                    "Lupus Anticoag": False
                }
            },
            "Immunology": {
                "Separate Brown Top Tube": {
                    "ANCA": False,
                    "ANA": False,
                    "Anti-Cardiolipin Abs": False,
                    "Liver Autoantibodies": False,
                    "TTGA/Coeliac": False,
                    "Total IgE": False
                }
            },
            "Other Tests": None
        },
        "Anti-Coagulant Therapy": None,
        "Collected By": None,
        "Date/Time Received": None,
        "Additional Information": "For details on tests and sample tube requirements, refer to https://esneftpathology.nhs.uk or call 0300 303 5299."
    }
    return form_data

def log_instance_of_document(data_structure: dict) -> dict[str, any]:
    """NOTE: I don't know what to do here yet."""
    # Dummy data will be a blood test result doument.

    system_prompt = ""
    query = ""
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
            ]
    )
    print(response.choices[0].message.content)

def main():
    # File paths
    pdf_path = os.path.join(os.getcwd(), "backend", "data", "test.pdf")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                print(page.extract_text())
    except FileNotFoundError as e:
        print(f"Error: Could not find PDF file - {e}")
    # openai_get_datastructure("data/test.pdf")
    # log_instance_of_document(hardcoded_datastructure())
if __name__ == "__main__":
    main()