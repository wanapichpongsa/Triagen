# SEE before_5pm branch for hackathon version

### Install dependencies

We're using [uv](https://docs.astral.sh/uv/getting-started/installation/) instead of pip because it uses Rust and its faster.

Go to `pyproject.toml` to find the library names for the following command:

```bash
uv add $dependency1 $dependency2 $dependency3
```

### Complicated Document Interpretation Stuff

From `json` object designed by Gemini, we're then going to have a pipeline that writes python scripts to process the same document indefinitely, without having to spend on LLMs!

Solution: We need to use cv2 and numpy to find coordinates, and context from Gemini to extract the correct data. $1 per 6,000 documents is cheap though... so we COULD just solely rely on Gemini to process every single document.

##### Draft Template Matching Scripts
**Template Matching**
```python
import cv2
import numpy as np

def find_form_elements(template, form):
    # Use cv2.matchTemplate to find elements
    result = cv2.matchTemplate(form, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc  # Returns (x, y) coordinates

```

**Bounding boxes?**
```python
import pytesseract
from PIL import Image

def get_text_locations(image_path):
    # Get bounding boxes and text
    data = pytesseract.image_to_data(Image.open(image_path), output_type=pytesseract.Output.DICT)
    
    coordinates = []
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:  # Confidence threshold
            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]
            coordinates.append({
                'text': data['text'][i],
                'bbox': (x, y, w, h)
            })
    return coordinates
```

**Form Processing Libraries**
```python
class BloodTestFormProcessor:
    def __init__(self, template_json):
        self.template = template_json
        self.coordinates = {
            "nhs_number": (10, 20, 100, 40),  # x1, y1, x2, y2
            "hospital_number": (120, 20, 250, 40),
            # ... other field coordinates
        }
    
    def process_image(self, image):
        results = {}
        for field, coords in self.coordinates.items():
            roi = image[coords[1]:coords[3], coords[0]:coords[2]]
            text = ocr_engine.process(roi)  # Using traditional OCR
            results[field] = text
        return results
```