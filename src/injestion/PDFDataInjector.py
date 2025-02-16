# Importing the required libraries
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.InjectionUtility import InjectionUtility
from src.conf.Configurations import logger
from src.database_utilities.Semantic_Table import SemanticTable
import os


class PDFDataInjector:

    @staticmethod
    def process_pdf_and_store( pdf_path):
        """
        This function extracts text from the specified PDF and stores the chunks in the database.
        :param pdf_path: The path to the PDF file.
        :return: None
        """

        # Get the file name
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Check if the document already exists in the database
        if SemanticTable().document_exists(file_name):
            logger.info(f"Document '{file_name}' already exists in the database. Skipping...")
            return

        # Extract text from PDF
        logger.info("Extracting text from PDF...")
        text = PDFDataExtractor().extract_text(pdf_path)

        # Process the text pipeline
        logger.info("Processing text pipeline...")
        InjectionUtility().process_text_pipeline(text, file_name)

        # Commit and close the database connection
        logger.info("closing the database connection...")
        SemanticTable().close()

# Run the script
if __name__ == "__main__":

    # Sample PDF path
    sample_pdf_path = r'C:\Docs\sample.pdf'

    # Process the PDF and store the chunks in the database
    PDFDataInjector().process_pdf_and_store(sample_pdf_path)
