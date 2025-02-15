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

# Remove if you want to use ElevenLabs agent
def construct_message(message_constructor: dict) -> str:
    from openai import OpenAI
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that constructs messages for an ElevenLabs agent."},
            {"role": "user", "content": "Output only the message, nothing else. message_constructor: " + str(message_constructor)}
            ]
    )


from dotenv import load_dotenv
import os
import requests

load_dotenv()
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

"""
OLLIE: get the correct API endpoint and API key please
method 1: https://elevenlabs.io/docs/conversational-ai/customization/personalization/dynamic-variables
method 2: https://elevenlabs.io/docs/conversational-ai/customization/tools/server-tools
"""
def text_to_speech(message: str) -> dict:
    BASE_URL = "https://api.elevenlabs.io/"
    url = f"{BASE_URL}v2/text-to-speech/convert"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {elevenlabs_api_key}"
    }
    body = {
        "text": message,
        "model_id": "eleven_turbo_v2_5",
        "output_format": "mp3_44_16000"
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

def main():
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

    patient_fullname = "John Doe"
    consultant = "Dr.Henry Williams"
    test_outcome = get_fbc_guidance(patient_data)

    message_constructor = {
        "patient_fullname": patient_fullname,
        "consultant": consultant,
        "test_outcome": test_outcome,
    }

    # RUNNING FUNCTIONS
    input_message = construct_message(message_constructor)
    print("Creating Input Message:\n", input_message)
    audio_response = text_to_speech(input_message)
    print("POST to Eleven Labs:\n", audio_response)

if __name__ == "__main__":
    main()