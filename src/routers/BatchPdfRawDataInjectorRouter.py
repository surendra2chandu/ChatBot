# Importing necessary libraries
from fastapi import APIRouter
from src.injestion.BatchPdfRawDataInjector import BatchPdfRawDataInjector

# Initialize the router
router = APIRouter(tags=["Batch-Injection"])

# Define the route for the root endpoint
@router.post("/pdf/raw_batch_data_injection/")
async def inject_raw_batch_pdf_data(path: str):
    """
    Function to inject data from a batch of PDF files into the database
    :param path: The path to the directory containing PDF files
    :return: The response from the service
    """

    # Inject data from the batch of PDF files into the database
    BatchPdfRawDataInjector().process_files(path)

    return "Data injected successfully"