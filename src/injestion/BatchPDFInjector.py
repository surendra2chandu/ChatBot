# Importing the required libraries
from src import logger
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.InjectionUtility import InjectionUtility
from src.database_utilities.Semantic_Table import SemanticTable
import os
from fastapi import HTTPException


class BatchPDFInjector:

    @staticmethod
    def get_pdf_files(directory_path: str):
        """
        Returns a list of all PDF files in the given directory.

        :param directory_path: Path to the directory containing PDF files.
        :return: List of PDF file paths.
        """

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

    @staticmethod
    def process_pdf_and_store( file, file_name):
        """
        Extracts text from the PDF and stores the processed chunks in the database.
        :param file: Path to the PDF file.
        :param file_name: Name of the file.
        :return: None
        """

        # Extract text from PDF
        logger.info(f"Extracting text from PDF: {file}")
        text = PDFDataExtractor().extract_text_from_pdf(file)

        if not text:
            logger.warning(f"No text extracted from {file}. Skipping...")
            return

        # Process the text pipeline
        logger.info("Processing text pipeline...")
        InjectionUtility().process_text_pipeline(text, file_name)

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
                if SemanticTable().document_exists(file_name):
                    logger.info(f"Document '{file_name}' already exists in the database. Skipping...")
                    continue
                # Process each PDF file
                logger.info(f"Processing PDF file: {file}")
                self.process_pdf_and_store(file, file_name)
            except Exception as e:
                # Log the error and raise an exception
                logger.error(f"An error occurred while processing {file}: {e}")
                raise HTTPException(status_code=500, detail=f"An error occurred while processing {file}: {e}")

        # Commit and close the database connection
        logger.info("closing the database connection...")
        SemanticTable().close()

# Run the script
if __name__ == "__main__":
    pdf_directory = r'C:\Docs'  # Update with your directory path
    BatchPDFInjector().process_files(pdf_directory)
