import cv2
import numpy as np

def png_to_contours(png_path):
    """
    Process a PNG image, detect edges, and find contours.
    """
    # Load the image
    image = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply edge detection (Canny)
    edges = cv2.Canny(image, 100, 200)
    
    # Find contours (shapes)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    print(f"Detected {len(contours)} shapes in the image.")
    return contours
	