# neon_styling.py

# Ensure necessary libraries are installed: pip install Pillow svgpathtools numpy
from PIL import Image, ImageDraw, ImageFilter
# --- Corrected Import Line (Removed 'Move') ---
from svgpathtools import svg2paths, Line, Arc, CubicBezier, QuadraticBezier
import os

# Helper function to parse color strings (R,G,B)
def parse_color(color_str, default_color=(255, 255, 255)):
    if isinstance(color_str, tuple) and len(color_str) == 3:
        return color_str # Already a tuple
    try:
        r, g, b = map(int, color_str.split(','))
        return (r, g, b)
    except Exception:
        print(f"Warning: Invalid color string '{color_str}'. Using default {default_color}.")
        return default_color

def create_neon_circle(output_path,
                       line_color="255,255,255", # White
                       line_width=5,
                       glow_radius=10,
                       glow_alpha=0.5,
                       size=(400, 400)):
    """
    Creates an image file with a simple neon circle effect.

    Args:
        output_path (str): Path to save the output PNG image.
        line_color (str/tuple): Color for the neon tube (e.g., "255,0,255" or (255,0,255)).
        line_width (int): Width/thickness of the neon tube.
        glow_radius (int): Radius for the Gaussian blur glow effect.
        glow_alpha (float): Blending alpha for the glow (0=sharp, 1=blur).
        size (tuple): (width, height) of the output image.
    """
    try:
        color = parse_color(line_color, (255, 255, 255)) # Default white
        background_color = (0, 0, 0)  # Black background
        img = Image.new("RGB", size, background_color)
        draw = ImageDraw.Draw(img)

        circle_center = (size[0] // 2, size[1] // 2)
        # Adjust radius based on size, ensure width doesn't exceed radius
        circle_radius = min(size[0], size[1]) // 2 - (line_width * 2)
        circle_radius = max(10, circle_radius) # Ensure minimum radius

        # Define bounding box for the ellipse
        bounding_box = [
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius,
        ]
        # Draw the sharp outline
        draw.ellipse(
            bounding_box,
            fill=None, # No fill
            outline=color, # Use parsed color
            width=line_width, # Use parameter
        )

        # Apply glow effect using Gaussian Blur and Blending
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=glow_radius)) # Use parameter
        # Blend the sharp image with the blurred image
        final_img = Image.blend(img, blurred_img, alpha=glow_alpha) # Use parameter

        # Ensure output directory exists before saving
        output_dir = os.path.dirname(output_path)
        if output_dir: # Check if path includes a directory
             os.makedirs(output_dir, exist_ok=True)

        final_img.save(output_path)

    except Exception as e:
        print(f"Error in create_neon_circle saving to {output_path}: {e}")


def apply_neon_effect(contours, output_path, image_size=(400, 400),
                      line_color="255,0,255", # Magenta
                      line_width=5,
                      glow_radius=10,
                      glow_alpha=0.5):
    """
    Applies neon effect to a list of contours (e.g., from OpenCV).

    Args:
        contours (list): List of contours from OpenCV.
        output_path (str): Path to save the output PNG image.
        image_size (tuple): (width, height) of the canvas.
        line_color (str/tuple): Color for the neon tube.
        line_width (int): Width/thickness of the neon tube.
        glow_radius (int): Radius for the Gaussian blur glow effect.
        glow_alpha (float): Blending alpha for the glow (0=sharp, 1=blur).
    """
    try:
        color = parse_color(line_color, (255, 0, 255)) # Default magenta
        background_color = (0, 0, 0)  # Black background
        img = Image.new("RGB", image_size, background_color)
        draw = ImageDraw.Draw(img)

        # Draw each contour
        for contour in contours:
            points = [tuple(point[0]) for point in contour]
            if len(points) > 1:
                draw.line(points, fill=color, width=line_width) # Use parameters
            elif len(points) == 1:
                draw.point(points[0], fill=color) # Use parameter

        # Apply glow effect
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=glow_radius)) # Use parameter
        final_img = Image.blend(img, blurred_img, alpha=glow_alpha) # Use parameter

        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
             os.makedirs(output_dir, exist_ok=True)

        final_img.save(output_path)

    except Exception as e:
        print(f"Error in apply_neon_effect saving to {output_path}: {e}")


# ==============================================================================
# === apply_neon_to_svg function with Parameterization ===
# ==============================================================================
def apply_neon_to_svg(svg_path, output_path, canvas_size=(400, 400), num_steps=25,
                      line_color="0,255,255", # Cyan
                      line_width=3,
                      glow_radius=8,
                      glow_alpha=0.6):
    """
    Apply neon effects to SVG paths by discretizing segments and drawing them.

    Args:
        svg_path (str): Path to the input SVG file.
        output_path (str): Path to save the output PNG image.
        canvas_size (tuple): (width, height) of the output image.
        num_steps (int): Number of points to sample along curves/arcs.
        line_color (str/tuple): Color for the neon tube.
        line_width (int): Width/thickness of the neon tube.
        glow_radius (int): Radius for the Gaussian blur glow effect.
        glow_alpha (float): Blending alpha for the glow (0=sharp, 1=blur).
    """
    print("DEBUG: Entered apply_neon_to_svg function.")
    try:
        print(f"DEBUG: Parsing SVG file '{svg_path}'...")
        paths, attributes = svg2paths(svg_path)
        print(f"Found {len(paths)} paths in the SVG.")
    except Exception as e:
        print(f"Error parsing SVG file '{svg_path}': {e}")
        return

    try:
        color = parse_color(line_color, (0, 255, 255)) # Default cyan
        print(f"DEBUG: Creating image canvas {canvas_size}...")
        img = Image.new("RGB", canvas_size, (0, 0, 0)) # Black background
        draw = ImageDraw.Draw(img)

        print(f"DEBUG: Processing SVG paths with color={color}, width={line_width}...")
        for path_index, path in enumerate(paths):
            print(f"DEBUG: Processing Path {path_index+1}/{len(paths)}")
            if not path: continue

            points_in_current_subpath = []
            start_of_current_subpath = None

            for segment_index, segment in enumerate(path):
                if not points_in_current_subpath:
                    if hasattr(segment, 'start'):
                         current_point = segment.start
                    else:
                         print(f"Warning: Cannot determine start point for segment type {type(segment)} at index {segment_index} in Path {path_index+1}")
                         continue

                    start_of_current_subpath = current_point
                    points_in_current_subpath.append((int(current_point.real), int(current_point.imag)))

                if isinstance(segment, Line):
                    points_in_current_subpath.append((int(segment.end.real), int(segment.end.imag)))
                elif isinstance(segment, (Arc, CubicBezier, QuadraticBezier)):
                    for i in range(1, num_steps + 1):
                        t = i / num_steps
                        p = segment.point(t)
                        points_in_current_subpath.append((int(p.real), int(p.imag)))
                elif isinstance(segment, Close):
                     if start_of_current_subpath is not None:
                         points_in_current_subpath.append((int(start_of_current_subpath.real), int(start_of_current_subpath.imag)))

                     if len(points_in_current_subpath) > 1:
                         draw.line(points_in_current_subpath, fill=color, width=line_width) # Use parameters

                     points_in_current_subpath = []
                     start_of_current_subpath = None

            if len(points_in_current_subpath) > 1:
                draw.line(points_in_current_subpath, fill=color, width=line_width) # Use parameters

        print(f"DEBUG: Applying glow effect (radius={glow_radius}, alpha={glow_alpha})...")
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=glow_radius)) # Use parameter
        final_img = Image.blend(img, blurred_img, alpha=glow_alpha) # Use parameter

        output_dir = os.path.dirname(output_path)
        if output_dir:
             os.makedirs(output_dir, exist_ok=True)

        print(f"DEBUG: Saving final image to {output_path}...")
        final_img.save(output_path)
        print(f"Saved neon SVG visualization to {output_path}")

    except Exception as e:
        print(f"Error processing or saving neon SVG image for {svg_path}: {e}")

# ==============================================================================
