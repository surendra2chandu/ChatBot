# Importing necessary libraries
from fastapi import APIRouter
from src.retrival.Retrival import Retrival

# Initialize the router
router = APIRouter(tags=["retrival"])


@router.post("/retrieve/similer_documents/")
async def get_similer_documents(query: str):
    """
    Function to get similer documents for the given query
    :param query: The query for which to find similer documents
    :return: The similer documents
    """

    # Get similer documents for the given query
    similer_documents = Retrival().get_similer_documents(query)

    return similer_documents
