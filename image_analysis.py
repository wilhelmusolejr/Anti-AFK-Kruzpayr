from keras.layers import TFSMLayer
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
from skimage.metrics import structural_similarity as ssim
from datetime import datetime
import tensorflow as tf

import numpy as np
import cv2
import mss
import pyautogui
import os

main_model = None
game_model = None

def get_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Use the primary monitor
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.rgb)

def pil_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def isInLobby(img_path_lobby_reference):
    screenshot = get_screenshot()
    img1 = pil_to_cv2(screenshot)
    img2 = cv2.imread(img_path_lobby_reference)

    if img2 is None:
        raise FileNotFoundError(f"Reference image '{img_path_lobby_reference}' not found.")

    # Convert to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Resize reference image to match screenshot if necessary
    if img1_gray.shape != img2_gray.shape:
        img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]))

    score, _ = ssim(img1_gray, img2_gray, full=True)
    print(f"SSIM Score: {score:.4f}")
    return score > 0.5

def state():
    global main_model
    
    if main_model is None:
        main_model = TFSMLayer("machine learning\main\model.savedmodel", call_endpoint="serving_default")
    
    # Load class labels
    with open("machine learning\main\labels.txt", "r") as f:
        class_names = [line.strip().split(' ', 1)[-1] for line in f]
    
    screenshot = get_screenshot()
    img1 = pil_to_cv2(screenshot)  # Converts PIL to OpenCV format (NumPy)

    # ✅ Convert OpenCV image (NumPy) back to PIL format correctly
    image = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

    # Resize + crop to 224x224 (as expected by your model)
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # Normalize image data
    image_array = np.asarray(image).astype(np.float32)
    normalized_image_array = (image_array / 127.5) - 1.0

    # Add batch dimension
    data = np.expand_dims(normalized_image_array, axis=0)

    # Predict
    prediction = main_model(data)

    # Extract tensor
    prediction_tensor = list(prediction.values())[0]
    prediction_array = prediction_tensor.numpy()

    # Interpret results
    index = np.argmax(prediction_array[0])
    class_name = class_names[index]
    confidence_score = prediction_array[0][index]
    
    print(f"Predicted class: {class_name} with confidence: {confidence_score:.4f}")

    if confidence_score >= 0.9:
        return class_name
    else:
        return None

def isPlayerValidWalk():
    global game_model
    
    if game_model is None:
        game_model = TFSMLayer("machine learning\game\model.savedmodel", call_endpoint="serving_default")
        
    # Load class labels
    with open("machine learning\game\labels.txt", "r") as f:
        class_names = [line.strip().split(' ', 1)[-1] for line in f]
    
    screenshot = get_screenshot()
    img1 = pil_to_cv2(screenshot)  # Converts PIL to OpenCV format (NumPy)

    # ✅ Convert OpenCV image (NumPy) back to PIL format correctly
    image = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))

    # Resize + crop to 224x224 (as expected by your model)
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # Normalize image data
    image_array = np.asarray(image).astype(np.float32)
    normalized_image_array = (image_array / 127.5) - 1.0

    # Add batch dimension
    data = np.expand_dims(normalized_image_array, axis=0)

    # Predict
    prediction = game_model(data)

    # Extract tensor
    prediction_tensor = list(prediction.values())[0]
    prediction_array = prediction_tensor.numpy()

    # Interpret results
    index = np.argmax(prediction_array[0])
    class_name = class_names[index]
    confidence_score = prediction_array[0][index]
    
    return class_name == "good"

def saveScreenshot(path = ""):
    folder = "screenshots" +  "/" + path
    os.makedirs(folder, exist_ok=True)  # create folder if not exists
    
    # Timestamp filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"screenshot_{timestamp}.png")
    
    # Take screenshot and save
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    
    print(f"✅ Screenshot saved: {filename}")

def crop_image(image, x, y, width, height):
    # Define the crop box: (left, upper, right, lower)
    crop_box = (x, y, x + width, y + height)
    cropped_image = image.crop(crop_box)
    return cropped_image

def is_killing(screenshot_path):
    # Open the image using PIL
    image = Image.open(screenshot_path)

    # Crop it
    cropped = crop_image(image, 300, 0, 500, 200)

    # Convert PIL image to OpenCV (numpy array)
    cropped = np.array(cropped)

    # Convert RGB to BGR (because PIL opens in RGB but OpenCV uses BGR)
    cropped = cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR)

    # Now continue with OpenCV
    kill_reference = cv2.imread("kill.png")

    # Convert to grayscale
    img1_gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(kill_reference, cv2.COLOR_BGR2GRAY)

    # Resize reference image if needed
    if img1_gray.shape != img2_gray.shape:
        img2_gray = cv2.resize(img2_gray, (img1_gray.shape[1], img1_gray.shape[0]))

    # Compute SSIM
    score, _ = ssim(img1_gray, img2_gray, full=True)
    print(f"SSIM Score: {score:.4f}")
    return score > 0.5

