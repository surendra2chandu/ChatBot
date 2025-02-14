# import necessary libraries
import requests
from src.conf.Configurations import logger, RETRIEVAL_URL, SEMANTIC_CONFIGURATION
from src.utilities.OllamaServiceManager import process_ollama_request
from src.utilities.ChatBotUtilities import get_sematic_similer_documents_text, get_tf_idf_similer_documents_text


def get_response(query):
    """
    Function to get response from the LateChunking service
    :param query: The query to be processed
    :return: The response from the service
    """

    response  = requests.post(RETRIEVAL_URL, params={"query": query})
    if response.status_code == 200:

        # Get the similer documents
        logger.info("Getting the similer documents...")
        similer_documents = response.json()

        if SEMANTIC_CONFIGURATION == "BOTH":

            # Get the text from the semantically similer documents and the Tf-Idf similer documents
            logger.info("Getting the text from the semantically similer documents and the Tf-Idf similer documents...")
            context = get_sematic_similer_documents_text(similer_documents) + get_tf_idf_similer_documents_text(similer_documents)

        elif SEMANTIC_CONFIGURATION == "Tf_Idf":

            # Get the text from the Tf-Idf similer documents
            logger.info("Getting the text from the Tf-Idf similer documents...")
            context = get_tf_idf_similer_documents_text(similer_documents)

        else:

            # Get the text from the semantically similer documents
            logger.info("Getting the text from the semantically similer documents...")
            context = get_sematic_similer_documents_text(similer_documents)

        if context:
            # Process the response with the Ollama model
            logger.info("Processing the response with the Ollama model")
            response = process_ollama_request(context, query)
        else:
            response = "No relevant information found in the database."

        return response

    else:
        return "Error occurred when processing the request to url " + RETRIEVAL_URL


if __name__ == "__main__":

    res = get_response("Who are the customers impacted by the upcoming satellite change for the AFN TV programming package in the Pacific region?")

    print(res)
