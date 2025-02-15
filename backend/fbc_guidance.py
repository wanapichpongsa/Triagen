import json

def get_fbc_guidance(patient_data: dict) -> str:
    with open('backend/fbc_guidance.json', 'r') as file:
        fbc_guidance = json.load(file)
    
    message = ""
    
    if patient_data["abnormality"] == "Anaemia":
        if (patient_data["gender"] == "male" and patient_data["hb"] < 130) or \
           (patient_data["gender"] == "female" and patient_data["hb"] < 115):
            message = f"Anaemia Referral: {fbc_guidance['Anaemia']['referral']['haematologist']}"

    elif patient_data["abnormality"] == "Polycythaemia":
        if (patient_data["gender"] == "male" and patient_data["hb"] > 185 and patient_data["hct"] > 0.52) or \
           (patient_data["gender"] == "female" and patient_data["hb"] > 160 and patient_data["hct"] > 0.48):
            message = f"Polycythaemia Referral: {fbc_guidance['Polycythaemia']['referral']['haematologist']}"

    elif patient_data["abnormality"] == "Eosinophilia":
        if patient_data["eosinophils"] > 1.5:
            message = f"Eosinophilia Referral: {fbc_guidance['Eosinophilia']['referral']['haematologist']}"

    elif patient_data["abnormality"] == "Lymphocytes":
        if patient_data["lymphocyte_count"] < 1.3:
            message = f"Lymphopenia Referral: {fbc_guidance['Lymphocytes']['abnormalities']['Lymphopenia']['referral']}"
        elif patient_data["lymphocyte_count"] > 20:
            message = f"Lymphocytosis Referral: {fbc_guidance['Lymphocytes']['abnormalities']['Lymphocytosis']['referral']}"

    elif patient_data["abnormality"] == "Neutrophils":
        if patient_data["neutrophil_count"] < 1.0:
            message = f"Severe Neutropenia Referral: {fbc_guidance['Neutrophils']['abnormalities']['Neutropenia']['referral']['urgent']}"
        elif 1.0 <= patient_data["neutrophil_count"] <= 1.5:
            message = f"Mild Neutropenia - Monitor and Repeat FBC: {fbc_guidance['Neutrophils']['abnormalities']['Neutropenia']['referral']['monitor']}"
        elif patient_data["neutrophil_count"] > 15:
            message = f"Neutrophilia Referral: {fbc_guidance['Neutrophils']['abnormalities']['Neutrophilia']['referral']}"

    elif patient_data["abnormality"] == "Platelets":
        if patient_data["platelets"] < 20:
            message = f"Thrombocytopenia Urgent Referral: {fbc_guidance['Platelets']['abnormalities']['Thrombocytopenia']['referral']['urgent']}"
        elif 50 <= patient_data["platelets"] <= 100:
            message = f"Thrombocytopenia - Monitor: {fbc_guidance['Platelets']['abnormalities']['Thrombocytopenia']['referral']['monitor']}"
        elif patient_data["platelets"] > 600:
            message = f"Thrombocytosis Urgent Referral: {fbc_guidance['Platelets']['abnormalities']['Thrombocytosis']['referral']['urgent']}"

    return message if message else None

from dotenv import load_dotenv
import os
import requests

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

"""
OLLIE: get the correct API endpoint and API key please
"""
def get_patient_data(tree_outcome: str) -> dict:
    BASE_URL = "https://api.elevenlabs.io/"
    url = f"{BASE_URL}v1/text-to-speech/convert"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {elevenlabs_api_key}"
    }
    response = requests.post(url, headers=headers, json={"text": tree_outcome})
    return response.json()

patient_data = {
    "abnormality": "Anaemia",   # could be "Anaemia", "Polycythaemia", etc.
    "gender": "male",
    "hb": 125,       # haemoglobin level
    "hct": 0.50,     # haematocrit level
    "eosinophils": 0.5,
    "lymphocyte_count": 1.0,
    "neutrophil_count": 0.9,
    "platelets": 80
}

tree_outcome = get_fbc_guidance(patient_data)

patient_data = get_patient_data(tree_outcome)
print("POST to Eleven Labs:\n", patient_data)