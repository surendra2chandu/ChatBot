# Importing necessary libraries
from fastapi import APIRouter
from src.retrival.Retrival import Retrival

# Initialize the router
router = APIRouter(tags=["retrival"])


@router.post("/retrieve/similar_documents/")
async def get_similar_documents(query: str, doc_id):
    """
    Function to get similar documents for the given query
    :param query: The query for which to find similar documents
    :param doc_id: The document id
    :return: The similar documents
    """

    # Get similar documents for the given query
    similar_documents = Retrival().get_similar_documents(query, doc_id)

    return similar_documents
