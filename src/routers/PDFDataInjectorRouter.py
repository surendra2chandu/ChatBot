# Importing necessary libraries
from fastapi import APIRouter
from src.ingestion.PDFDataInjector import PDFDataInjector

# Initialize the router
router = APIRouter(tags=["Injection"])

# Define the route for the root endpoint
@router.post("/pdf/injection/")
async def inject_pdf_data(pdf_path: str):
    """
    Function to inject data from a PDF file into the database
    :param pdf_path: The path to the PDF file
    :return: The response from the service
    """

    # Inject data from the PDF file into the database
    PDFDataInjector.process_pdf_and_store(pdf_path)

    return "Data injected successfully"
