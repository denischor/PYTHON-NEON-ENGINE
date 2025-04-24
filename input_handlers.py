# input_handlers.py

# Ensure necessary libraries are installed:
# pip install opencv-python Pillow pdf2image numpy
# Requires Poppler binaries installed and in PATH for pdf2image
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import tempfile # For handling temporary images from PDF/Text

# Attempt to import pdf2image, handle if not installed
try:
    from pdf2image import convert_from_path
    PDF2IMAGE_INSTALLED = True
except ImportError:
    PDF2IMAGE_INSTALLED = False
    print("Warning: pdf2image library not found. PDF processing will be unavailable.")
    print("Install it using: pip install pdf2image")
    print("Also ensure Poppler is installed and in your system PATH.")

# --- Refactored PNG Contour Detection ---
def get_contours_from_image(image_path):
    """
    Detects contours in an image file (e.g., PNG).

    Args:
        image_path (str): Path to the input image file.

    Returns:
        list: List of detected contours (OpenCV format), or None if error.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        print(f"Error: Could not load image at {image_path}")
        return None # Return None on error

    # --- Contour Detection Logic (same as before) ---
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 100, 200) # Adjust thresholds as needed
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Detected {len(contours)} shapes in the image '{os.path.basename(image_path)}'.")
    return contours

# --- PDF Handler ---
def get_contours_from_pdf(pdf_path, page_num=0):
    """
    Converts the first page of a PDF to an image and detects contours.

    Args:
        pdf_path (str): Path to the input PDF file.
        page_num (int): The page number to process (0-indexed). Default is 0 (first page).

    Returns:
        tuple: (list of contours, tuple image_size) or (None, None) if error.
               Image size (width, height) is needed for apply_neon_effect.
    """
    if not PDF2IMAGE_INSTALLED:
        print("Error: pdf2image is required for PDF processing but not installed.")
        return None, None

    try:
        # Convert the specified page of the PDF to a PIL Image
        # Use first=page_num+1 and last=page_num+1 for 1-based indexing in pdf2image
        images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)

        if not images:
            print(f"Error: Could not convert page {page_num} from PDF '{pdf_path}'.")
            return None, None

        pil_image = images[0]
        image_size = pil_image.size # Get (width, height)

        # Convert PIL image to OpenCV format (BGR)
        open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # --- Use the same contour detection logic ---
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        print(f"Detected {len(contours)} shapes in page {page_num} of PDF '{os.path.basename(pdf_path)}'.")
        return contours, image_size

    except Exception as e:
        print(f"Error processing PDF file '{pdf_path}': {e}")
        # Check if it's a Poppler error
        if "poppler" in str(e).lower():
             print("This might indicate Poppler is not installed or not in the system PATH.")
        return None, None


# --- Text Handler ---
def get_contours_from_text(text_string, font_path=None, font_size=60, image_size=(400, 400)):
    """
    Renders text onto an image and detects contours.

    Args:
        text_string (str): The text to render.
        font_path (str, optional): Path to a .ttf font file. Defaults to Pillow's basic font.
        font_size (int): Font size in points.
        image_size (tuple): (width, height) of the canvas to render text on.

    Returns:
        tuple: (list of contours, tuple image_size) or (None, None) if error.
    """
    try:
        # Create a black canvas
        img = Image.new('RGB', image_size, color = (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Load font
        try:
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Use default Pillow font if specific one not found/provided
                print("Warning: Font path not provided or invalid. Using default font.")
                font = ImageFont.load_default() # Note: Default font is small
        except IOError:
            print(f"Error: Could not load font at {font_path}. Using default.")
            font = ImageFont.load_default()

        # Calculate text position (simple centering)
        # Use textbbox for more accurate positioning with newer Pillow versions
        try:
            # Pillow >= 9.2.0
            bbox = draw.textbbox((0, 0), text_string, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        except AttributeError:
            # Older Pillow versions
            text_width, text_height = draw.textsize(text_string, font=font)

        x = (image_size[0] - text_width) / 2
        y = (image_size[1] - text_height) / 2

        # Draw the text in white
        draw.text((x, y), text_string, font=font, fill=(255, 255, 255))

        # Convert PIL image to OpenCV format (BGR)
        open_cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # --- Use the same contour detection logic ---
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        # Note: Blurring might be less necessary or even detrimental for sharp text
        # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Adjust Canny thresholds for text if needed
        edges = cv2.Canny(gray, 50, 150) # Might need different thresholds than for general images
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        print(f"Detected {len(contours)} shapes from the text.")
        return contours, image_size

    except Exception as e:
        print(f"Error processing text string: {e}")
        return None, None

# --- Original png_to_contours can now just call get_contours_from_image ---
# --- Keeping it separate allows specific logic for PNGs if needed later ---
def png_to_contours(png_path):
     """
     Wrapper function specifically for PNG files.
     Detects contours in a PNG file.

     Args:
         png_path (str): Path to the input PNG file.

     Returns:
         list: List of detected contours (OpenCV format), or None if error.
     """
     return get_contours_from_image(png_path)

