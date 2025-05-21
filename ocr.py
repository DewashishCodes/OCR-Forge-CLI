import pytesseract
from PIL import Image
import os
# We will need the TESSERACT_CMD path from config, but set it here.

def set_tesseract_cmd(path):
     """Sets the path to the Tesseract executable."""
     pytesseract.pytesseract.tesseract_cmd = path
     # Optional: Add a check or print message
     # print(f"Tesseract command set to: {pytesseract.pytesseract.tesseract_cmd}")

def extract_text_from_image(image_path):
    """Extracts text from a given image file using Tesseract."""
    if not os.path.exists(image_path):
         print(f"❌ Image file not found for OCR: {image_path}")
         return "[Image File Not Found Error for OCR]"

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except pytesseract.TesseractNotFoundError:
        # If tesseract_cmd was set but the executable isn't there
        print(f"❌ Tesseract executable not found at {pytesseract.pytesseract.tesseract_cmd}")
        print("   Please ensure Tesseract is installed and the path is correct in config.py")
        return "[Tesseract Not Found Error]"
    except Exception as e:
         print(f"❌ Error during OCR extraction from {image_path}: {e}")
         return f"[OCR Extraction Error]: {e}"