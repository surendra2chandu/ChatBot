# Importing necessary libraries
from fastapi import APIRouter
from src.api.TextSummarizer import TextSummarizer

# Initialize the router
router = APIRouter(tags=["text-summarizer"])

@router.post("/summarize/")
async def get_summary(doc_id: str):
    """
    Function to get summary of the given text
    :param doc_id: The document id
    :return: The summary of the text
    """

    # Get summary of the given text
    summary = TextSummarizer().summarize(doc_id)

    return summary

