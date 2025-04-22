from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np
import pyautogui
import time

def pil_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def isInLobby(pil_img1, img2_path):
    img1 = pil_to_cv2(pil_img1)
    img2 = cv2.imread(img2_path)

    # Convert to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(img1_gray, img2_gray, full=True)
    return score > 0.5






