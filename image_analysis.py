from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
from PIL import Image
import mss
import time

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