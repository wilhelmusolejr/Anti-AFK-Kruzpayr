from skimage.metrics import structural_similarity as ssim
import cv2

def isInLobby(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Convert to grayscale
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    score, _ = ssim(img1_gray, img2_gray, full=True)
    return score > 0.5




