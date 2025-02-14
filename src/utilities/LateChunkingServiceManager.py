#import necessary libraries
import requests
from src.conf.Configurations import logger, LATE_CHUNKING_URL, THRESHOLD

def get_response_from_late_chunking(query):
    """
    Function to get response from the LateChunking service
    :param query: The query to be processed
    :return: The response from the service
    """

    # Initialize the context
    context = ""

    # Send a post request to the LateChunking service and get the response
    logger.info(f"Sending a post request to the LateChunking service with query: {query}")
    late_chunk_response = requests.post(LATE_CHUNKING_URL, params={"query": query})
    if late_chunk_response.status_code == 200:

        # Get the response in JSON format
        response = late_chunk_response.json()

        for i in range(len(response)):
            if response[i][1] >= THRESHOLD:
                # Append the relevant information to the context
                logger.info(f"Appending relevant information to the context")
                context += response[i][0] + ". \n"

        return context
    else:
        response = f"Error occurred when processing the request to url {LATE_CHUNKING_URL}"

        return response


if __name__ == "__main__":

    res = get_response_from_late_chunking("Who are the customers impacted by the upcoming satellite change for the AFN TV programming package in the Pacific region?")

    print(res)
