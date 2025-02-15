import os
from dotenv import load_dotenv

from openai import OpenAI
import json
import requests

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
ragie_api_key = os.getenv("RAGIE_API_KEY")

# API Configuration
BASE_URL = "https://api.ragie.ai"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/documents"
RETRIEVALS_ENDPOINT = f"{BASE_URL}/retrievals"

def get_datastructure():
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
    
    formatted_json = json.dumps(document_chunks.json(), indent=2)
    document_id = "f4ac0e9d-01f4-4f6d-ad68-ad7a14801266"
    
    # Extract text for specific document ID
    ragie_response = next(
        (chunk["text"] for chunk in document_chunks.json()["scored_chunks"] 
         if chunk["document_id"] == document_id),
        None
    )
    
    print(ragie_response)
    """
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Return the datastructure of this medical document in dictionary format."}
        ]
    )
    print(response.choices[0].message.content)
    """

def bloodtest_structure():
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


def log_query(data_structure: dict):
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
    get_datastructure()

if __name__ == "__main__":
    main()