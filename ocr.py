import pytesseract
import cv2
import numpy as np
from PIL import Image

# Set path to Tesseract executable (update this path to match your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load the image (can be a screenshot or file)
image_path = "Crossfire20250412_0016.bmp"  # or "screenshot.png"
image = cv2.imread(image_path)

# Preprocess the image (optional: improves OCR accuracy)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Convert to PIL format for pytesseract
pil_img = Image.fromarray(thresh)

# Perform OCR
custom_config = r'--psm 6'
text = pytesseract.image_to_string(pil_img, config=custom_config)

# Output the result
print("🎯 Detected Text:", text.strip())
