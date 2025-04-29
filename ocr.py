import pytesseract
import cv2
import numpy as np

from PIL import Image, ImageOps
from image_analysis import crop_image, get_screenshot

# Set path to Tesseract executable (update this path to match your system)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def userRoomStatus():
    screenshot = get_screenshot()
    
    # Crop first directly on PIL image
    cropped = crop_image(screenshot, 670, 420, 120, 40)

    # Convert to grayscale directly using PIL
    gray_cropped = ImageOps.grayscale(cropped)

    # Optional: Apply thresholding using simple point operation (faster than OpenCV)
    thresh_cropped = gray_cropped.point(lambda p: 255 if p > 150 else 0)

    # Perform OCR
    custom_config = r'--psm 7'  # psm 7 = Treat image as a single line of text (more aggressive and faster)
    text = pytesseract.image_to_string(thresh_cropped, config=custom_config)

    # Join Game
    # Ready!
    # Start
    # Cancel
    
    return text.strip().lower()

def get_exp():
    screenshot = get_screenshot()
    
    # Crop first directly on PIL image
    cropped = crop_image(screenshot, 640, 300, 140, 20)

    # Convert to grayscale directly using PIL
    gray_cropped = ImageOps.grayscale(cropped)

    # Optional: Apply thresholding using simple point operation (faster than OpenCV)
    thresh_cropped = gray_cropped.point(lambda p: 255 if p > 150 else 0)

    # Perform OCR
    custom_config = r'--psm 7'  # psm 7 = Treat image as a single line of text (more aggressive and faster)
    text = pytesseract.image_to_string(thresh_cropped, config=custom_config)

    return text.strip().lower()

def get_gp():
    screenshot = get_screenshot()
    
    # Crop first directly on PIL image
    cropped = crop_image(screenshot, 640, 270, 140, 20)

    # Convert to grayscale directly using PIL
    gray_cropped = ImageOps.grayscale(cropped)

    # Optional: Apply thresholding using simple point operation (faster than OpenCV)
    thresh_cropped = gray_cropped.point(lambda p: 255 if p > 150 else 0)

    # Perform OCR
    custom_config = r'--psm 7'  # psm 7 = Treat image as a single line of text (more aggressive and faster)
    text = pytesseract.image_to_string(thresh_cropped, config=custom_config)

    return text.strip().lower()

def get_kill():
    screenshot = get_screenshot()
    
    # Crop first directly on PIL image
    cropped = crop_image(screenshot, 470, 30, 100, 50)

    # Convert to grayscale directly using PIL
    gray_cropped = ImageOps.grayscale(cropped)

    # Optional: Apply thresholding using simple point operation (faster than OpenCV)
    thresh_cropped = gray_cropped.point(lambda p: 255 if p > 150 else 0)

    # Perform OCR
    custom_config = r'--psm 7'  # psm 7 = Treat image as a single line of text (more aggressive and faster)
    text = pytesseract.image_to_string(thresh_cropped, config=custom_config)

    return text.strip().lower()
    