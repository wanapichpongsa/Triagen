import os
from dotenv import load_dotenv
import requests
import json
from openai import OpenAI

# API Configuration
BASE_URL = "https://api.ragie.ai"
DOCUMENTS_ENDPOINT = f"{BASE_URL}/documents"
INSTRUCTIONS_ENDPOINT = f"{BASE_URL}/instructions"
QUERY_ENDPOINT = f"{BASE_URL}/retrievals"

load_dotenv()
ragie_api_key = os.getenv("RAGIE_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {ragie_api_key}"
}

def get_documents() -> None:
    response = requests.get(DOCUMENTS_ENDPOINT, headers=headers)
    print(response.text + "\n")

def create_instructions() -> None:
    instruction_data = {
        "name": "Medical Triage Assessment",
        "active": True,
        "scope": "document",
        "prompt": "Analyze the patient's symptoms and medical history for triage assessment.",
        "entity_schema": {
            "type": "object",
            "properties": {
                "urgency_level": {
                    "type": "string",
                    "enum": ["priority_1", "priority_2", "priority_3", "priority_4", "priority_5"]
                },
                "symptoms": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "recommended_action": {
                    "type": "string",
                    "enum": ["emergency", "urgent_care", "primary_care", "self_care"] # or could be forms of medical treatment
                }
            },
            "required": ["urgency_level", "symptoms", "recommended_action"]
        }
    }

    response = requests.post(INSTRUCTIONS_ENDPOINT, headers=headers, json=instruction_data)
    print(response.text+ "\n")

def bloodtest_structure():
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


def log_query(RAGIE_RETRIEVAL: str):
    # Dummy data will be a blood test result doument.
    data = RAGIE_RETRIEVAL

    system_prompt = 
    query = 
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
    get_documents()
    create_instructions()

if __name__ == "__main__":
    main()