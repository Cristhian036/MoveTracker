import cv2
import easyocr
import os
import numpy as np

# Initialize the reader once (it loads the model into memory)
# 'en' is usually sufficient for license plates (numbers + letters)
# gpu=True uses your RTX 3050 Ti
try:
    reader = easyocr.Reader(['en'], gpu=True)
except Exception as e:
    print(f"Warning: Could not initialize EasyOCR with GPU: {e}")
    reader = easyocr.Reader(['en'], gpu=False)

def preprocess_plate(image):
    """
    Apply image processing to improve OCR accuracy.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Resize (Zoom) - making it bigger helps OCR
    scale_percent = 200 # percent of original size
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(gray, dim, interpolation = cv2.INTER_CUBIC)
    
    # Apply thresholding to get black text on white background (or vice versa)
    # Otsu's thresholding is usually good
    _, thresh = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def read_plate_text(image_path_or_array):
    """
    Reads text from a license plate image.
    Args:
        image_path_or_array: File path (str) or numpy array (cv2 image)
    Returns:
        list of tuples: [(bbox, text, prob), ...]
    """
    if isinstance(image_path_or_array, str):
        if not os.path.exists(image_path_or_array):
            print(f"Error: File {image_path_or_array} not found.")
            return []
        img = cv2.imread(image_path_or_array)
    else:
        img = image_path_or_array

    if img is None:
        print("Error: Could not load image.")
        return []

    # Preprocess
    processed_img = preprocess_plate(img)

    # Read text
    # allowlist: restrict to uppercase letters and numbers for plates
    results = reader.readtext(processed_img, 
                              allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-',
                              detail=1)
    
    return results
