# Make sure these imports are at the top of your neon_styling.py file
from svgpathtools import svg2paths, Line, Arc, CubicBezier, QuadraticBezier
from PIL import Image, ImageDraw, ImageFilter # <-- Added ImageFilter here

def apply_neon_to_svg(svg_path, output_path, canvas_size=(400, 400), num_steps=25):
    """
    Apply neon effects to SVG paths by discretizing and drawing segments.

    Args:
        svg_path (str): Path to the input SVG file.
        output_path (str): Path to save the output PNG image.
        canvas_size (tuple): (width, height) of the output image.
        num_steps (int): Number of steps to discretize curves/arcs. More steps = smoother.
    """
    try:
        # Parse the SVG file to get path objects
        paths, attributes = svg2paths(svg_path)
        print(f"Found {len(paths)} paths in the SVG.")
    except Exception as e:
        print(f"Error parsing SVG file '{svg_path}': {e}")
        return

    # Create a black canvas
    img = Image.new("RGB", canvas_size, (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define drawing style
    line_color = (0, 255, 255)  # Cyan
    line_width = 3             # Adjust thickness as needed

    # Process each path object found in the SVG
    for path in paths:
        if not path: continue # Skip empty paths

        points_in_current_subpath = []
        start_of_current_subpath = None

        for segment in path:
            # Determine the start point for this segment
            if not points_in_current_subpath: # Starting a new subpath
                if isinstance(segment):
                    current_point = segment.end
                elif hasattr(segment, 'start'):
                     current_point = segment.start
                else:
                     continue # Cannot determine start point
                start_of_current_subpath = current_point # Remember start for Close
                points_in_current_subpath.append((int(current_point.real), int(current_point.imag)))


            # Generate points for the segment
            if isinstance(segment, Line):
                # Line just needs the end point
                points_in_current_subpath.append((int(segment.end.real), int(segment.end.imag)))
            elif isinstance(segment, (Arc, CubicBezier, QuadraticBezier)):
                # Discretize curves/arcs into small steps
                for i in range(1, num_steps + 1):
                    t = i / num_steps
                    p = segment.point(t) # Get point along the segment at position t (0 to 1)
                    points_in_current_subpath.append((int(p.real), int(p.imag)))
            elif isinstance(segment, Close):
                # Close the path by connecting back to the start of this subpath
                if start_of_current_subpath is not None:
                    points_in_current_subpath.append((int(start_of_current_subpath.real), int(start_of_current_subpath.imag)))
                # Draw this completed subpath and reset for the next one
                if len(points_in_current_subpath) > 1:
                    draw.line(points_in_current_subpath, fill=line_color, width=line_width)
                points_in_current_subpath = []
                start_of_current_subpath = None
            elif isinstance(segment):
                 # Draw the previous subpath before moving
                 if len(points_in_current_subpath) > 1:
                      draw.line(points_in_current_subpath, fill=line_color, width=line_width)
                 # Start new subpath list
                 current_point = segment.end
                 start_of_current_subpath = current_point
                 points_in_current_subpath = [(int(current_point.real), int(current_point.imag))]


        # Draw any remaining points after the last segment if the path wasn't closed
        if len(points_in_current_subpath) > 1:
            draw.line(points_in_current_subpath, fill=line_color, width=line_width)

    # Apply glow effect (Blur and blend)
    try:
        blurred_img = img.filter(ImageFilter.GaussianBlur(radius=8)) # Adjust radius for glow size
        # Blend the original sharp lines with the blurred version
        final_img = Image.blend(img, blurred_img, alpha=0.6) # Adjust alpha for glow intensity
        final_img.save(output_path)
        print(f"Saved neon SVG visualization to {output_path}")
    except Exception as e:
        print(f"Error applying blur or saving final image: {e}")
        