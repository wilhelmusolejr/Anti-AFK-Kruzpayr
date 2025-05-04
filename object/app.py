from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import mss
import time
import os

# Load model
model = YOLO("object/my_model.pt")

def get_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Use the primary monitor
        sct_img = sct.grab(monitor)
        return Image.frombytes('RGB', sct_img.size, sct_img.rgb)

def get_object_location():
    # Take screenshot and convert to OpenCV format
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    pil_image = get_screenshot()

    # Save raw screenshot
    os.makedirs("screenshots", exist_ok=True)
    raw_path = f"screenshots/screenshot_{timestamp}.png"
    pil_image.save(raw_path)

    # Convert to OpenCV format
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Run inference
    results = model(image)

    # Draw first detected box only
    for result in results:
        boxes = result.boxes
        if len(boxes) == 0:
            return None  # No detections

        box = boxes[0]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        # Draw box and label
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = model.names[int(box.cls[0])]
        cv2.putText(image, f"{label} ({cx}, {cy})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # 🔴 Draw red dot at the center
        cv2.circle(image, (cx, cy), 5, (0, 0, 255), -1)

        # Save image with box and red dot
        boxed_path = f"screenshots/screenshot_with_box_{timestamp}.png"
        cv2.imwrite(boxed_path, image)

        return {
            "center": (cx, cy),
            "box": (x1, y1, x2, y2),
            "label": label
        }

    return None  # Fallback if no result
