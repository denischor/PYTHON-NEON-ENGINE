from pdf2image import convert_from_path

def pdf_to_images(pdf_path, output_dir):
    """
    Convert a PDF file to images (one image per page).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Specify the Poppler path explicitly
    poppler_path = r'C:\Users\Administrator\poppler-24.08.0\Library\bin'
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, output_folder=output_dir, poppler_path=poppler_path)
        
        # Save each page as an image
        for i, image in enumerate(images):
            image_path = os.path.join(output_dir, f'page_{i+1}.png')
            image.save(image_path, 'PNG')
            print(f"Saved page {i+1} as {image_path}")
        
        return [os.path.join(output_dir, f'page_{i+1}.png') for i in range(len(images))]
    except Exception as e:
        print(f"Error converting PDF: {e}")
        return []
        import logging
logging.basicConfig(level=logging.DEBUG)

from pdf2image import convert_from_path

try:
    images = convert_from_path('example.pdf', output_folder='./output_images')
except Exception as e:
    print(f"Error converting PDF: {e}")
    
	
    