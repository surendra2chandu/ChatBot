# Importing necessary libraries
from fastapi import APIRouter
from src.retrival.Retrival import Retrival

# Initialize the router
router = APIRouter(tags=["retrival"])


@router.post("/retrieve/similer_documents/")
async def get_similer_documents(query: str, doc_id):
    """
    Function to get similer documents for the given query
    :param query: The query for which to find similer documents
    :param doc_id: The document id
    :return: The similer documents
    """

    # Get similer documents for the given query
    similer_documents = Retrival().get_similer_documents(query, doc_id)

    return similer_documents
