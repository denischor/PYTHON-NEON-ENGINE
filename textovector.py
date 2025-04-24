from PIL import Image, ImageDraw, ImageFont

def text_to_image(text, font_path, output_path):
    """
    Render text into an image.
    """
    # Create an image with the text
    img = Image.new('RGB', (500, 200), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, size=40)
    draw.text((10, 10), text, font=font, fill=(0, 0, 0))
    
    # Save the image
    img.save(output_path)
    print(f"Rendered text '{text}' to {output_path}")
	