import os # Added for checking directories/files if needed

# Assuming these functions are defined correctly in their respective files
from neon_styling import create_neon_circle, apply_neon_effect, apply_neon_to_svg
from input_handlers import png_to_contours # Contains the png_to_contours function

# Define output directory and ensure it exists
output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True) # Create dir if it doesn't exist

# --- Test neon circle ---
print("Testing neon circle creation...")
neon_circle_path = os.path.join(output_dir, 'neon_circle.png')
try:
    # Assuming create_neon_circle saves the file itself
    create_neon_circle(neon_circle_path)
    # The print statement from your original trace indicates success here
    print(f"Saved neon circle to {neon_circle_path}")
except Exception as e:
    print(f"Error creating neon circle: {e}")


# --- Test neon effect for contours (Original Line 8 is updated below) ---
print("\nTesting PNG to image contours...")

# IMPORTANT: Make sure 'example.png' exists and is a VALID png file!
# Remember the previous errors with example.pdf suggested file corruption issues.
contour_input_path = 'example.png'
contour_output_path = os.path.join(output_dir, 'neon_contours.png')

try:
    # === THIS IS THE CORRECTED LINE ===
    # Call the function using the keyword argument 'output_path='
    contours_list = png_to_contours(contour_input_path, output_path=contour_output_path)
    # The png_to_contours function prints success/failure messages internally

except FileNotFoundError:
     print(f"Error: Input file not found at {contour_input_path}")
except Exception as e:
     # Catch other potential errors from the function or file saving
     print(f"An unexpected error occurred calling png_to_contours: {e}")


# --- Test neon effect for SVG paths ---
print("\nTesting neon effect for SVG...")
# IMPORTANT: Make sure 'example.svg' exists and is a valid SVG file.
svg_input_path = 'example.svg'
svg_output_path = os.path.join(output_dir, 'neon_svg.png')
try:
    # Assuming apply_neon_to_svg works correctly and saves the file
    apply_neon_to_svg(svg_input_path, svg_output_path)
    print(f"Applied neon effect to SVG and saved to {svg_output_path}")
except FileNotFoundError:
    print(f"Error: Input file not found at {svg_input_path}")
except Exception as e:
    print(f"An error occurred applying neon effect to SVG: {e}")


print("\nFinished tests.")
