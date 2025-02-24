# Import necessary libraries
import fitz
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
import re

class PDFDataExtractor:

    def __init__(self):

        # Set the path to tesseract.exe (Only needed for Windows users)
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


    @staticmethod
    def preprocess_image( image):
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


    def extract_text(self, pdf_path):
        """Extract both text and text from images in a PDF while preserving order."""
        doc = fitz.open(pdf_path)  # Open PDF
        extracted_text = ""

        for page_number in range(len(doc)):
            page = doc[page_number]
            text = page.get_text("text")  # Extract text from the page
            page_text = ""
            if text.strip():
                page_text += text.strip() + "\n"

            images = page.get_images(full=True)  # Get all images on the page

            for img_index, img in enumerate(images):
                xref = img[0]  # Get image reference
                base_image = doc.extract_image(xref)  # Extract image data
                image_bytes = base_image["image"]

                # Convert to PIL Image
                image = Image.open(io.BytesIO(image_bytes))

                # Preprocess image for better text recognition
                processed_image = self.preprocess_image(image)

                # Extract text using OCR
                img_text = pytesseract.image_to_string(processed_image, lang="eng", config="--psm 3 --oem 3")


                # Check if text is meaningful
                if img_text.strip():
                    page_text += img_text.strip() + "\n"

            extracted_text += page_text  # Append text from the current page


        extracted_text = re.sub(r'\s+', ' ', extracted_text.strip())
        # Remove all extra special characters, keeping only one
        extracted_text = re.sub(r'([^\w\s])\1+', r'\1', extracted_text)

        # Remove any characters that aren't alphanumeric, spaces, or single special characters
        extracted_text = re.sub(r'[^\w\s.,?!]', '', extracted_text)

        return extracted_text


if __name__ == '__main__':
    pdf_data_extractor = PDFDataExtractor()
    sample_pdf_path = r'C:\Docs1\D.pdf'
    text = pdf_data_extractor.extract_text(sample_pdf_path)
    print(text)