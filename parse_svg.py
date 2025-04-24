from svgpathtools import svg2paths

def parse_svg(file_path):
    """
    Parse an SVG file and extract its paths.
    """
    paths, attributes = svg2paths(file_path)
    print(f"Found {len(paths)} paths in the SVG.")
    return paths, attributes

# Example usage
if __name__ == "__main__":
    # Path to your SVG file
    svg_file = 'example.svg'
    
    # Parse the SVG file
    paths, attributes = parse_svg(svg_file)
    
    # Print the number of paths found
    print(f"Found {len(paths)} paths in the SVG.")
    