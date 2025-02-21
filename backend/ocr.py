import os
import pytesseract
from PIL import Image, ImageEnhance
import cv2
import numpy as np
from dotenv import load_dotenv

def preprocess_image(image):
    # Convert PIL Image to cv2 format
    opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoisingColored(opencv_image)
    
    # Convert to grayscale
    gray = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
    
    # Thresholding to get black and white image
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Deskew if needed
    # Find coordinates of all non-black pixels (text)
    # np.where returns row,col arrays of white pixels
    # column_stack combines them into (x,y) coordinate pairs
    coords = np.column_stack(np.where(threshold > 0))

    # Find minimum area rectangle that contains all text
    # minAreaRect returns ((center_x, center_y), (width, height), angle)
    # [-1] gets just the angle of text rotation
    angle = cv2.minAreaRect(coords)[-1]

    # Convert angle to -45 to 45 degree range
    # If angle is less than -45, adding 90 gives the
    # complementary angle for shortest rotation path
    if angle < -45:
        angle = 90 + angle

    # Get image dimensions and calculate center point
    # Center will be the pivot point for rotation
    (h, w) = threshold.shape[:2]
    center = (w // 2, h // 2)

    # Create transformation matrix for rotating image
    # Parameters: center point, angle, scale (1.0 = no scaling)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Apply rotation to image using transformation matrix
    # warpAffine rotates using the matrix M
    # INTER_CUBIC = smooth interpolation for better quality
    # BORDER_REPLICATE = extends border pixels to fill empty corners
    rotated = cv2.warpAffine(threshold, M, (w, h), 
                            flags=cv2.INTER_CUBIC, 
                            borderMode=cv2.BORDER_REPLICATE)
    
    # Convert back to PIL Image
    return Image.fromarray(rotated)

def multi_pass_ocr(image):
    texts = []
    
    # Try different PSM modes
    psm_modes = [1, 3, 6]  # Auto, Auto+OSD, Uniform block
    for psm in psm_modes:
        config = f'--oem 3 --psm {psm}'
        text = pytesseract.image_to_string(image, config=config)
        texts.append(text)
    
    # Return the longest text (usually the most complete)
    return max(texts, key=len)

def image_to_text(filename: str, debug: bool = False) -> str:
    try:
        image = Image.open(f"database/data/{filename}")
        preprocessed_image = preprocess_image(image)
        extracted_text = multi_pass_ocr(preprocessed_image)
        if debug:
            with open(f"database/debug/{filename}_ocr_results.txt", 'w') as f:
                f.write(extracted_text)
        return extracted_text
    except Exception as e:
        print(f"Error in image_to_text: {e}")
        raise

from google import genai
load_dotenv()

def gemini_vision(filename: str, debug: bool = False) -> str:
    image = Image.open(f"database/data/{filename}")
    if not image:
        raise ValueError("Image not found")
    api_key = os.getenv("GEMINI_API")
    if not api_key:
        raise ValueError("GEMINI_API environment variable not set")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["Only extract the text from the image and only output a JSON object of the image structure", image])
    if debug:
        with open(f"database/debug/{filename}_gemini_results.txt", 'w') as f:
            f.write(response.text)
    return response.text


def main():
    print(gemini_vision("woundcare.png", debug=True))
    # print(image_to_text("bloodtest-form.png"))
    # print("\n\n\n\n\n")
    # print(image_to_text("woundcare.png", debug=True))

if __name__ == "__main__":
    main()