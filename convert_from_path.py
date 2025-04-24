from pdf2image import convert_from_path
import os

def pdf_to_images(pdf_path, output_dir):
    """
    Convert a PDF file to images (one image per page).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert PDF to images
    images = convert_from_path(pdf_path)
    
    # Save each page as an image
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f'page_{i+1}.png')
        image.save(image_path, 'PNG')
        print(f"Saved page {i+1} as {image_path}")
    
    return [os.path.join(output_dir, f'page_{i+1}.png') for i in range(len(images))]
	