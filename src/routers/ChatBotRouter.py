# Importing necessary libraries
from fastapi import APIRouter
from src.api.ChatBot import ChatBot


# Initialize the router
router = APIRouter(tags=["chatbot"])

# Define the route for the root endpoint
@router.post("/chatbot/")
async def get_chatbot_response(query: str, doc_id: str):
    """
    Function to get response from the ChatBot service
    :param query: The query to be processed
    :param doc_id: The document id
    :return: The response from the service
    """

    # Get the response from the ChatBot service
    response = ChatBot().get_response(query, doc_id)

    return response