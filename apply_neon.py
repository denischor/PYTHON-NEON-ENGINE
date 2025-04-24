# apply_neon.py

import argparse
import os
import sys

# Import necessary functions from your other modules
# Ensure neon_styling now has the parameterized functions
from neon_styling import apply_neon_effect, apply_neon_to_svg, create_neon_circle # Added create_neon_circle if needed
from input_handlers import (
    get_contours_from_image,
    get_contours_from_pdf,
    get_contours_from_text
)

# Helper function (can be moved to neon_styling if preferred)
def parse_color_arg(color_str):
    """Parses R,G,B string, returns tuple or raises error."""
    try:
        r, g, b = map(int, color_str.split(','))
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError("Color values must be between 0 and 255.")
        return (r, g, b)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Invalid color format '{color_str}'. Use R,G,B (e.g., '255,0,255'). Error: {e}")

def main():
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="Apply neon effect to various input types.")
    parser.add_argument("input_path", help="Path to the input file (PNG, SVG, PDF, TXT) or 'circle' for test circle.")
    parser.add_argument("output_path", help="Path to save the output neon PNG image.")

    # Input specific args
    parser.add_argument("-p", "--page", type=int, default=0,
                        help="Page number to process for PDF files (0-indexed, default: 0).")
    parser.add_argument("-t", "--text", type=str, default=None, # Default None, use file content first
                        help="Text string to use (overrides text file content if provided).")
    parser.add_argument("-f", "--font", type=str, default=None,
                        help="Path to .ttf font file for text rendering.")
    parser.add_argument("-fs", "--fontsize", type=int, default=60,
                        help="Font size for text rendering.")

    # Canvas size args
    parser.add_argument("--width", type=int, default=400,
                        help="Canvas width for text/PDF/SVG rendering.")
    parser.add_argument("--height", type=int, default=400,
                        help="Canvas height for text/PDF/SVG rendering.")

    # --- NEW Styling Arguments ---
    parser.add_argument("--color", type=str, default="255,0,255", # Default Magenta as string
                        help="Neon tube color as R,G,B (e.g., '0,255,255' for cyan).")
    parser.add_argument("--linewidth", type=int, default=5,
                        help="Width/thickness of the neon tube.")
    parser.add_argument("--glowradius", type=int, default=10,
                        help="Radius for the Gaussian blur glow effect.")
    parser.add_argument("--glowalpha", type=float, default=0.5,
                        help="Blending alpha for the glow (0.0=sharp only, 1.0=blur only).")
    # --- End NEW Styling Arguments ---

    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    canvas_size = (args.width, args.height)

    # Parse color argument safely
    try:
         line_color_tuple = parse_color_arg(args.color)
    except argparse.ArgumentTypeError as e:
         print(f"Error: {e}")
         sys.exit(1)

    # Store styling parameters in a dictionary for easier passing
    style_params = {
        "line_color": line_color_tuple, # Pass the parsed tuple
        "line_width": args.linewidth,
        "glow_radius": args.glowradius,
        "glow_alpha": args.glowalpha
    }

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # --- Determine Input Type and Process ---
    is_file_input = input_path.lower() != 'circle' and os.path.exists(input_path)
    extension = ""
    if is_file_input:
        _, extension = os.path.splitext(input_path)
        extension = extension.lower()

    print(f"Processing input: {input_path}")

    contours = None
    image_size_for_effect = canvas_size # Default size

    # Handle special 'circle' input
    if input_path.lower() == 'circle':
         print("Input type: Test Circle")
         create_neon_circle(output_path, size=canvas_size, **style_params)
         print(f"Processing complete. Output saved to {output_path}")
         sys.exit(0)

    # Handle file inputs
    elif is_file_input:
        if extension == ".svg":
            print("Input type: SVG")
            apply_neon_to_svg(input_path, output_path, canvas_size=canvas_size, **style_params)
            print(f"Processing complete. Output saved to {output_path}")
            sys.exit(0) # Exit after SVG processing

        elif extension == ".png":
            print("Input type: PNG")
            try:
                from PIL import Image
                with Image.open(input_path) as img:
                    image_size_for_effect = img.size
            except Exception as e:
                 print(f"Warning: Could not read PNG size, using default {canvas_size}. Error: {e}")
            contours = get_contours_from_image(input_path)

        elif extension == ".pdf":
            print("Input type: PDF")
            contours, pdf_image_size = get_contours_from_pdf(input_path, page_num=args.page)
            if pdf_image_size:
                 image_size_for_effect = pdf_image_size

        elif extension == ".txt":
            print("Input type: Text File")
            text_content = args.text # Use command-line text if provided
            if text_content is None: # Only read file if --text wasn't used
                 try:
                     with open(input_path, 'r', encoding='utf-8') as f:
                         text_content = f.read().strip()
                         if not text_content:
                              print(f"Warning: Text file '{input_path}' is empty. Using default text 'Neon!'.")
                              text_content = "Neon!" # Fallback if file is empty
                 except Exception as e:
                     print(f"Error reading text file '{input_path}': {e}. Using default text 'Neon!'.")
                     text_content = "Neon!" # Fallback on read error

            contours, text_image_size = get_contours_from_text(
                text_content,
                font_path=args.font,
                font_size=args.fontsize,
                image_size=canvas_size
            )
            image_size_for_effect = text_image_size

        else:
            print(f"Error: Unsupported file type '{extension}'. Please use .png, .svg, .pdf, .txt or 'circle'.")
            sys.exit(1)

    # Handle case where input path was given but not found (and not 'circle')
    elif not is_file_input and args.text is not None:
         print("Input type: Direct Text (Input path ignored)")
         text_content = args.text
         contours, text_image_size = get_contours_from_text(
             text_content,
             font_path=args.font,
             font_size=args.fontsize,
             image_size=canvas_size
         )
         image_size_for_effect = text_image_size
    else:
        print(f"Error: Input path '{input_path}' not found or invalid.")
        sys.exit(1)


    # --- Apply Neon Effect (for PNG, PDF, TXT derived contours) ---
    if contours is not None:
        print(f"Applying neon effect to {len(contours)} contours...")
        # Pass the styling parameters using dictionary unpacking
        apply_neon_effect(contours, output_path, image_size=image_size_for_effect, **style_params)
        print(f"Processing complete. Output saved to {output_path}")
    else:
        print("No contours found or error occurred during contour detection. No output generated.")
        sys.exit(1)

if __name__ == "__main__":
    main()
