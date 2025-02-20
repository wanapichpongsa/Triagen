import os
from dotenv import load_dotenv

from openai import OpenAI
import json
import re
import hashlib
import psycopg2
from database.migrate import init_tables
from database.connection import get_db_connection

load_dotenv()

def create_hash(filename: str) -> tuple[str, str]:
    """Create and store file hash, returns (uuid, hash)"""
    try:
        with open(f"database/data/{filename}", "rb") as f:
            filehash = hashlib.md5(f.read()).hexdigest()
        
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO documents (filename, filehash)
                VALUES (%s, %s)
                RETURNING filehash
                """, (filename, filehash))
            conn.commit()
            return cur.fetchone()
            
    except Exception as e:
        print(f"Error creating hash: {e}")
        return None

def get_hash(hash: str) -> bool:
    """Check if document exists in processed_documents"""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM processed_documents 
            WHERE filehash = %s
            """, (hash,))
        result = cur.fetchone()
        return result is not None

def openai_get_datastructure(filename: str) -> str:
    system_prompt = "You are a medical form parser. Extract the form structure and return it as a JSON object."
    import pytesseract
    from PIL import Image

    try:
        # Read and encode image
        image = Image.open(f"database/data/{filename}")

        # Use OCR to extract text from the image
        extracted_text = pytesseract.image_to_string(image)
        if not extracted_text:
            raise Exception("No text extracted from image")
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Output only the JSON object, nothing else. extracted_text: {extracted_text}"}
            ],
            max_tokens=1000
        )
        message = response.choices[0].message.content
        
        # Validate that the response is valid JSON before saving
        try:
            json.loads(message, strict=False)  # Test if parseable
        except json.JSONDecodeError:
            raise Exception(f"OpenAI returned invalid JSON: {message}")

        # Save response for debugging
        os.makedirs("database/response", exist_ok=True)  # Create directory if it doesn't exist
        with open(f"database/response/openai_response_{filename}.json", "w") as f:
            f.write(message)
            
        return message

    except Exception as e:
        print(f"Error in openai_get_datastructure: {e}")
        raise

def edit_datastructure(data_structure: dict) -> dict:
    # editing GUI
    # tkinter?
    return {"test": "test"}
    
def log_instance_of_document(filename: str, data_structure: json) -> None:
    """Log document data to database and file system"""
    data_structure_json = json.dumps(data_structure, indent=4)
    
    path = f"database/format/format{filename}.json"
    with open(path, "w") as f:
        f.write(data_structure_json)
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT uuid, filehash FROM documents WHERE filename = %s
                """, (filename,))
            result = cur.fetchone()
            if not result:
                raise Exception("Error: Document not found in database.")
            uuid, hash = result
            cur.execute("""
                INSERT INTO processed_documents (doc_id, doc_uuid, data_structure)
                VALUES (%s, %s, %s)
                """, (uuid, hash, data_structure_json))
            conn.commit()
    except psycopg2.Error as e:
        print(f"Error logging document: {e}")
        raise

def engine(filename: str):
    # Create hash and store document
    hash = create_hash(filename)
    if not hash:
        print("Error creating hash. Exiting...")
        return
    if not get_hash(hash):
        response1: str = openai_get_datastructure(filename)
        json_data = json.loads(response1, strict=False) # allow control characters \n
        try:
            while True:
                continue_loop = input("Correct format? (y/n/exit)")
                if re.match(r"^y+e*s*$", continue_loop.lower()):
                    log_instance_of_document(filename, json_data)
                    break
                elif re.match(r"^n+o*$", continue_loop.lower()):
                    response1 = edit_datastructure(response1)
                elif re.match(r"^e+x+i+t*$", continue_loop.lower()):
                    break
                else:
                    print("Invalid input. Please enter 'y/yes', 'n/no', or 'exit'")
        except KeyboardInterrupt:
            print("Exiting...")
    else:
        print("File already exists in database.")

if __name__ == "__main__":
    engine("test.pdf")
    from fbc_guidance import fbc_main
    fbc_main()