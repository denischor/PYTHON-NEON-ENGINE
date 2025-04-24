import os
from input_handlers import parse_svg, pdf_to_images, png_to_contours, text_to_image

# Sample files
SVG_FILE = 'example.svg'
PDF_FILE = 'example.pdf'
PNG_FILE = 'example.png'
FONT_FILE = 'arial.ttf'

# Output directories
OUTPUT_DIR_PDF = './output_images'
OUTPUT_TEXT_IMAGE = 'output_text.png'

# Ensure output directories exist
if not os.path.exists(OUTPUT_DIR_PDF):
    os.makedirs(OUTPUT_DIR_PDF)

# Test SVG parsing
print("Testing SVG parsing...")
parse_svg(SVG_FILE)

# Test PDF to images conversion
print("\nTesting PDF to images conversion...")
pdf_to_images(PDF_FILE, OUTPUT_DIR_PDF)

# Test PNG contour detection
print("\nTesting PNG contour detection...")
png_to_contours(PNG_FILE)

# Test text rendering to image
print("\nTesting text rendering to image...")
text_to_image('Hello Neon', FONT_FILE, OUTPUT_TEXT_IMAGE)
