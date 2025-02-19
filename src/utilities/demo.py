# Import necessary libraries
import fitz
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np

# Set the path to tesseract.exe (Only needed for Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image):
    """
    Preprocess an image for better text recognition.
    :param image: PIL Image object.
    :return: Preprocessed image.
    """
    img = np.array(image)  # Convert PIL image to NumPy array


    # Ensure the image is in grayscale
    if image.mode == "L":  # Already grayscale
        gray = img
    elif image.mode in ["RGB", "RGBA"]:  # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        raise ValueError(f"Unexpected image mode: {image.mode}")

    # Apply thresholding for better OCR results
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return Image.fromarray(thresh)  # Convert back to PIL Image


def extract_text_from_pdf(pdf_path):
    """Extract both text and text from images in a PDF while preserving order."""
    doc = fitz.open(pdf_path)  # Open PDF
    extracted_text = ""

    for page_number in range(len(doc)):
        page = doc[page_number]
        text = page.get_text("text")  # Extract text from the page

        page_text = f"\n--- Page {page_number + 1} ---\n"
        if text.strip():
            page_text += f"\n[Text]\n{text.strip()}\n"

        images = page.get_images(full=True)  # Get all images on the page

        for img_index, img in enumerate(images):
            xref = img[0]  # Get image reference
            base_image = doc.extract_image(xref)  # Extract image data
            image_bytes = base_image["image"]

            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_bytes))

            # Preprocess image for better text recognition
            processed_image = preprocess_image(image)

            # Extract text using OCR
            img_text = pytesseract.image_to_string(processed_image, lang="eng", config="--psm 3 --oem 3")


            # Check if text is meaningful
            if img_text.strip():
                page_text += f"\n[Image {img_index + 1}]\n{img_text.strip()}\n"

        extracted_text += page_text  # Append text from the current page

    return extracted_text


# Example Usage
pdf_path = r"C:\Docs\demo2.pdf"
text_data = extract_text_from_pdf(pdf_path)

print("Extracted Text:\n", text_data)
