# Import the necessary packages
from PyPDF2 import PdfReader
from src.conf.Configurations import logger
import re

class PDFDataExtractor:

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file.
        :param pdf_path: Path to the PDF file.
        :return: Extracted text from the PDF file.
        """

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


if __name__ == '__main__':
    pdf_data_extractor = PDFDataExtractor()
    sample_pdf_path = r'C:\Docs\sample_doc.pdf'
    extracted_text = pdf_data_extractor.extract_text_from_pdf(sample_pdf_path)
    print(extracted_text)