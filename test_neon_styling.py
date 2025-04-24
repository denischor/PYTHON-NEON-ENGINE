# --- Start of test_neon_styling.py ---
from neon_styling import create_neon_circle, apply_neon_effect, apply_neon_to_svg
from input_handlers import png_to_contours
import os # Good practice

print("--- Script Start ---")

output_dir = 'output_images'
os.makedirs(output_dir, exist_ok=True)

# Test neon circle
print("DEBUG: Calling create_neon_circle...")
create_neon_circle(os.path.join(output_dir, 'neon_circle.png'))
print("DEBUG: Returned from create_neon_circle.")

# Test neon effect for contours
print("DEBUG: Calling png_to_contours...")
png_to_contours('example.png', output_path=os.path.join(output_dir, 'neon_contours.png'))
print("DEBUG: Returned from png_to_contours.") # Will print after function finishes

# Test neon effect for SVG paths
print("DEBUG: About to call apply_neon_to_svg...") # <-- ADD THIS LINE
apply_neon_to_svg('example.svg', os.path.join(output_dir, 'neon_svg.png'))
print("DEBUG: Returned from apply_neon_to_svg.") # <-- ADD THIS LINE

print("--- Script End ---")
# --- End of test_neon_styling.py ---

