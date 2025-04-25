from keras.layers import TFSMLayer
from tensorflow.keras.models import load_model
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Load the TFSMLayer model
model = TFSMLayer("saved_model_directory", call_endpoint="serving_default")

# Load class labels
with open("labels.txt", "r") as f:
    class_names = [line.strip().split(' ', 1)[-1] for line in f]


images = ["sample_score.bmp", "current.bmp", "lobby.bmp"]

for image in images:
    # Load and preprocess the image
    image = Image.open(image).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)

    # Convert to numpy and normalize
    image_array = np.asarray(image).astype(np.float32)
    normalized_image_array = (image_array / 127.5) - 1.0  # Normalize to [-1, 1]

    # Add batch dimension
    data = np.expand_dims(normalized_image_array, axis=0)

    # Predict
    prediction = model(data)  # Make the prediction

    # Access the tensor inside the dictionary and convert it to a NumPy array
    prediction_tensor = prediction['sequential_15']  # Assuming 'sequential_15' is the key
    prediction_array = prediction_tensor.numpy()  # Convert tensor to NumPy array

    # Get the index of the highest confidence score
    index = np.argmax(prediction_array[0])  # Get the index of the highest value in the first batch element

    # Get the predicted class and confidence score
    class_name = class_names[index]
    confidence_score = prediction_array[0][index]

    # Output the results
    print(f"Class: {class_name}")
    print(f"Confidence Score: {confidence_score:.2f}")
