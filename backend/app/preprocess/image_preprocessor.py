from PIL import Image, ImageEnhance, ImageFilter


def preprocess_image_for_ocr(file_path: str) -> Image.Image:
    """
    Preprocess an image to improve OCR accuracy.

    Steps:
    1. Open image
    2. Convert to grayscale
    3. Resize to improve readability
    4. Increase contrast
    5. Sharpen
    6. Apply thresholding
    """
    image = Image.open(file_path)

    # Convert to grayscale
    image = image.convert("L")

    # Resize image (2x bigger)
    width, height = image.size
    image = image.resize((width * 2, height * 2))

    # Increase contrast
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(2.0)

    # Sharpen image
    image = image.filter(ImageFilter.SHARPEN)

    # Thresholding (convert to black and white)
    image = image.point(lambda p: 255 if p > 180 else 0)

    return image