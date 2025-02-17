# Import the necessary packages
from src import logger
from PyPDF2 import PdfReader
import re
import fitz
from fastapi import HTTPException

class PDFDataExtractor:

    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """
        Extract text from a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text from the PDF file.
        """

        logger.info(f"Extracting text from PDF: {pdf_path}")

        # Read the PDF file
        reader = PdfReader(pdf_path)

        # Initialize the text
        text = ""

        # Iterate over the pages
        for page_number in range(len(reader.pages)):
            text += reader.pages[page_number].extract_text()

            # Remove extra spaces
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove all extra special characters, keeping only one
        text = re.sub(r'([^\w\s])\1+', r'\1', text)
        # Remove any characters that aren't alphanumeric, spaces, or single special characters
        text = re.sub(r'[^\w\s.,?!]', '', text)

        text = ' '.join(re.sub(r'[^A-Za-z0-9\s]', '', text).split())

        # Return the extracted text
        return text

    @staticmethod
    def extract_text(pdf_path):
        """
        Extract text from a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text from the PDF file.
        """
        try:
            # Open the PDF and extract text with cleaned formatting
            logger.info(f"Extracting text from PDF: {pdf_path}")
            doc = fitz.open(pdf_path)
            text = " ".join([page.get_text("text").strip().replace("\n", " ") for page in doc])

            # to-do get images data in pdf
            text = " ".join(text.split())

            return text
        except Exception as e:
            logger.info(f"Error occurred while extracting text from PDF: {e}")
            raise HTTPException(status_code=500, detail=f"Error occurred while extracting text from PDF: {e}")



if __name__ == '__main__':
    pdf_data_extractor = PDFDataExtractor()
    sample_pdf_path = r'C:\Docs\sample.pdf'
    extracted_text = pdf_data_extractor.extract_text(sample_pdf_path)
    print(extracted_text)