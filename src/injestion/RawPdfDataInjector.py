# Import the necessary libraries
from src import logger
from langchain.text_splitter import TokenTextSplitter
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.database_utilities.TfIdf_Table import TfIdfTable
from src.conf.Configurations import CHUNK_SIZE, CHUNK_OVERLAP
import os
from fastapi import HTTPException

class RawPdfDataInjector:

    @staticmethod
    def split_text_into_chunks(text):
        """
        Split text into meaningful chunks.
        :param text: The text to split.
        :return: A list of text chunks.
        """
        try:
            # Define LangChain Token Splitter
            logger.info("Splitting text into chunks...")
            token_splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

            # Split text into meaningful chunks
            chunks = token_splitter.split_text(text)

            return chunks
        except Exception as e:
            logger.error(f"Error during text splitting: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during text splitting: {e}")

    def process_pdf(self, pdf_path):
        """
        Extract, split, and store PDF data.
        :param pdf_path: The path to the PDF file.
        :return: None
        """

        # Get the file name
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Check if the document already exists in the database
        if TfIdfTable().document_exists(file_name):
            logger.info(f"Document '{file_name}' already exists in the database. Skipping...")
            return

        # Extract text from PDF
        logger.info("Extracting text from PDF...")
        text = PDFDataExtractor().extract_text(pdf_path)

        # Split text into chunks
        chunks = self.split_text_into_chunks(text)

        # Store chunks in the database
        logger.info("Storing chunks in the database...")
        TfIdfTable().store_chunks_in_db(file_name, chunks)

# Run the program
if __name__ == "__main__":
    sample_pdf_path = r'C:\Docs\gopichandnemalipuri_resume.pdf' # Replace with your PDF file path
    RawPdfDataInjector().process_pdf(sample_pdf_path)
