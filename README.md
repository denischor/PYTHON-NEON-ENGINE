# Python Neon Engine

A Python tool to automatically apply neon light effects to various input types like SVG paths, PNG image contours, PDF pages, and text.

## Features

* **Multi-Format Input:** Accepts SVG, PNG, PDF, and TXT files as input.
* **Neon Styling:** Applies neon tube outlines and glow effects.
* **Customizable Effects:** Allows control over neon color, line thickness, glow radius, and glow intensity via command-line arguments.
* **SVG Path Handling:** Processes complex SVG paths including lines, arcs, and Bezier curves using discretization.
* **Image Contour Handling:** Detects contours in PNG images (or images derived from PDF/text) using OpenCV.
* **PDF Processing:** Converts specified PDF pages to images for contour detection (requires Poppler).
* **Text Rendering:** Renders text strings using specified fonts and applies neon effects to the outlines.

*(Based on project goals, future features might include backplate generation, vector output (SVG/PDF), and more dynamic/editable controls)*

## Installation & Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone [https://github.com/denischor/PYTHON-NEON-ENGINE.git](https://github.com/denischor/PYTHON-NEON-ENGINE.git)
    cd PYTHON-NEON-ENGINE
    ```
    *(Replace the URL if needed)*

2.  **Create and Activate a Virtual Environment:** (Recommended)
    ```bash
    # Create the environment (e.g., named .venv)
    python -m venv .venv

    # Activate it
    # Windows (Command Prompt)
    .\.venv\Scripts\activate
    # Windows (PowerShell)
    .\.venv\Scripts\Activate.ps1
    # macOS / Linux
    # source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Poppler (for PDF support):**
    * `pdf2image` (used by the script) requires the Poppler PDF rendering library.
    * **Windows:** Download Poppler binaries, extract them, and add the `bin` folder to your system's PATH environment variable. (Refer to earlier conversation steps if needed).
    * **macOS (using Homebrew):** `brew install poppler`
    * **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install poppler-utils`

## Usage

The main script is `apply_neon.py`. Run it from the command line within the activated virtual environment.

**Basic Syntax:**

```bash
python apply_neon.py <input_path_or_circle> <output_path.png> [options]
Arguments:input_path_or_circle: Path to the input file (PNG, SVG, PDF, TXT) or the special keyword circle.output_path.png: Path where the output neon PNG image will be saved.Options:--color "R,G,B": Neon tube color (default: "255,0,255" - magenta). E.g., "0,255,255" for cyan.--linewidth INT: Neon tube thickness (default: 5).--glowradius INT: Glow effect blur radius (default: 10).--glowalpha FLOAT: Glow blend intensity (0.0 to 1.0, default: 0.5).--page INT: PDF page number (0-indexed, default: 0).--text "STRING": Text to render (overrides text file content).--font PATH: Path to a .ttf font file for text.--fontsize INT: Font size for text (default: 60).--width INT: Canvas width (default: 400).--height INT: Canvas height (default: 400).Examples:# Process an SVG with specific styling
python apply_neon.py example.svg output_images/neon_svg_custom.png --color "0,255,0" --linewidth 4 --glowradius 12

# Process a PNG
python apply_neon.py example.png output_images/neon_png.png

# Process page 1 of a PDF
python apply_neon.py document.pdf output_images/neon_pdf_p1.png -p 1

# Process a text file using Arial font
python apply_neon.py message.txt output_images/neon_text.png --font "C:\Windows\Fonts\arial.ttf" --fontsize 80 --color "255,165,0"

# Generate a test circle
python apply_neon.py circle output_images/test_circle.png --color "0,0,255"
Example Outputs(Optional: Consider adding a few example output images here if you commit them to the repository. Make sure the paths are correct relative to the README.md file)**SVG Input:**
![Neon SVG Example](output_images/neon_from_svg.png)

**Text Input (Arial Font):**
![Neon Text Example](output_images/neon_from_txt_arial.png)
DependenciesRequired Python libraries are listed in requirements.txt:Pillowopencv-pythonpdf2imagesvgpathtoolsnumpyExternal dependency:Poppler (for PDF processing via pdf2image)Future Work / TODOImplement backplate generation.Add vector export options (SVG, PDF).Implement more dynamic styling rules based on input characteristics.

