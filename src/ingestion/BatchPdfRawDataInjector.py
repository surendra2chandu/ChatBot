# Importing the required libraries
from src import logger
from src.utilities.PDFDataExtractor import PDFDataExtractor
import os
from fastapi import HTTPException
from src.conf.Configurations import CHUNK_SIZE, CHUNK_OVERLAP
from langchain.text_splitter import TokenTextSplitter
from src.database_utilities.TfIdf_Table import TfIdfTable

class BatchPdfRawDataInjector:

    @staticmethod
    def get_pdf_files(directory_path: str):
        """
        This function gets a list of all PDF files in the given directory.
        :param directory_path: Path to the directory containing PDF files.
        :return: List of PDF files in the directory.
        """
        try:
            # Check if the directory exists
            if not os.path.isdir(directory_path):
                raise HTTPException(status_code=400, detail=f"Invalid directory: {directory_path}")

            # Get a list of all PDF files in the directory
            logger.info(f"Getting PDF files in directory: {directory_path}")
            pdf_files = [
                os.path.join(directory_path, file)
                for file in os.listdir(directory_path)
                if file.lower().endswith('.pdf')
            ]

            # Log a warning if no PDF files are found
            if not pdf_files:
                logger.info(f"No PDF files found in {directory_path}")

            # Return the list of PDF files
            return pdf_files

        except Exception as e:
            # Log the error and raise an exception
            logger.error(f"An error occurred while getting PDF files: {e}")
            raise HTTPException(status_code=500,
                                detail=f"An error occurred while getting PDF files from {directory_path}: {e}")

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
            token_splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)  # Approx 500 chars

            # Split text into meaningful chunks
            chunks = token_splitter.split_text(text)

            return chunks

        except Exception as e:
            # Log the error and raise an exception
            logger.error(f"An error occurred while splitting text into chunks: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while splitting text into chunks: {e}")

    def process_pdf_and_store(self, file, file_name):
        """
        Extracts text from the PDF and stores the processed chunks in the database.
        :param file: Path to the PDF file.
        :param file_name: Name of the file.
        :return: None
        """

        # Extract text from PDF
        logger.info(f"Extracting text from PDF: {file}")
        text = PDFDataExtractor().extract_text(file)

        if not text:
            logger.warning(f"No text extracted from {file}. Skipping...")
            return

        # Split text into chunks
        chunks = self.split_text_into_chunks(text)

        # Store chunks in the database
        logger.info("Storing chunks in the database...")
        TfIdfTable().store_chunks_in_db(file_name, chunks)


    def process_files(self, directory_path):
        """
        Processes all PDF files in the given directory.
        :param directory_path: Path to the directory containing PDF files.
        :return: None
        """

        # Get a list of all PDF files in the directory
        logger.info(f"Processing PDF files in directory: {directory_path}")
        pdf_files = self.get_pdf_files(directory_path)

        for file in pdf_files:
            try:
                # Get the file name
                file_name = os.path.splitext(os.path.basename(file))[0]

                # Check if the document already exists in the database
                if TfIdfTable().document_exists(file_name):
                    logger.info(f"Document '{file_name}' already exists in the database. Skipping...")
                    continue
                # Process each PDF file
                logger.info(f"Processing PDF file: {file}")
                self.process_pdf_and_store(file, file_name)
            except Exception as e:
                # Log the error and raise an exception
                logger.error(f"An error occurred while processing {file}: {e}")
                raise HTTPException(status_code=500, detail=f"An error occurred while processing {file}: {e}")


# Run the program
if __name__ == "__main__":
    pdf_directory = r'C:\Docs'
    BatchPdfRawDataInjector().process_files(pdf_directory)
