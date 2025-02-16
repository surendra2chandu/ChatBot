# Import the necessary libraries
from langchain.text_splitter import TokenTextSplitter
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.database_utilities.TfIdf_Table import TfIdfTable
from src.conf.Configurations import logger ,CHUNK_SIZE, CHUNK_OVERLAP
import os


def split_text_into_chunks(text):
    """
    Split text into meaningful chunks.
    :param text: The text to split.
    :return: A list of text chunks.
    """

    # Define LangChain Token Splitter
    logger.info("Splitting text into chunks...")
    token_splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)  # Approx 500 chars

    # Split text into meaningful chunks
    chunks = token_splitter.split_text(text)

    return chunks


def process_pdf(pdf_path):
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
    chunks = split_text_into_chunks(text)

    # Store chunks in the database
    logger.info("Storing chunks in the database...")
    TfIdfTable().store_chunks_in_db(file_name, chunks)

# Run the program
if __name__ == "__main__":
    sample_pdf_path = r'C:\Docs\sample.pdf' # Replace with your PDF file path
    process_pdf(sample_pdf_path)
