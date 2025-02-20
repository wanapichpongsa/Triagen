import os
import pytesseract
from PIL import Image

def image_to_text(filename: str) -> str:
    image = Image.open(f"database/data/{filename}")
    text = pytesseract.image_to_string(image)
    return text

def main():
    print(image_to_text("bloodtest-form.png"))
    print("\n\n\n\n\n")
    print(image_to_text("woundcare.png"))

if __name__ == "__main__":
    main()