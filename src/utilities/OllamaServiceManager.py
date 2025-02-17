# Importing necessary classes
from src import logger
import requests
from fastapi import HTTPException
from src.conf.Configurations import OLLAMA_URL, OLLAMA_SUMMARIZATION_URL
import re


def process_ollama_request(context: str, question ):
    """
    This function sends a POST request to the Ollama service and returns the response.
    :param context: The context in which to answer the question.
    :param question: The question to answer.
    :return: The answer generated by the Ollama model.
    """

    # Define the questions
    questions = [question]

    # Define the data to be sent in the request body
    prompt = {
        "questions": questions,
        "context": context
    }

    # Send the POST request with JSON data and query parameter
    logger.info("Sending the POST request with JSON data and query parameter")
    response = requests.post(OLLAMA_URL, json=prompt)

    if response.status_code == 200:
        try:
            # Get the answer from the response
            logger.info("Getting the answer from the response")
            res = response.json()

            # Extract the answer from the response
            match = re.search(r"(?<=A:\s).*", res, re.DOTALL)

            return match.group()

        except Exception as e:
            logger.info(f"Error occurred while parsing the response: {e}")
            raise HTTPException(status_code=500, detail=f"Error occurred while parsing the response{e},"
                                                        f" and the response is {response.json()}")

    else:
        logger.error(f"Error occurred while sending the request: {response.text}")
        raise HTTPException(status_code=500, detail=f"Error occurred while sending the request: {response.text}")



def summarize_text(context: str):
    """
    This function sends a POST request to the Ollama service for text summarization and returns the response.
    :param context: The text to summarize.
    :return: The summarized text generated by the Ollama model.
    """


    # Send the POST request with JSON data and query parameter
    logger.info("Sending the POST request with JSON data and query parameter")
    response = requests.post(OLLAMA_SUMMARIZATION_URL, params={"context": context})

    if response.status_code == 200:
        try:
            # Get the answer from the response
            logger.info("Getting the answer from the response")
            res = response.json()

            return res

        except ValueError as e:
            logger.info(f"Error occurred while parsing the response: {e}")
            raise HTTPException(status_code=500, detail=f"Error occurred while parsing the response{e},"
                                                        f" and the response is {response.json()}")

    else:
        logger.info(f"Error occurred while sending the request: {response.text}")
        raise HTTPException(status_code=500, detail=f"Error occurred while sending the request: {response.text}")