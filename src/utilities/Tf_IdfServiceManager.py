#import necessary libraries
import requests
from src.conf.Configurations import logger, TF_IDF_URL, THRESHOLD


def get_response_tf_idf(query):
    """
    Function to get response from the Tf-Idf service
    :param query: The query to be processed
    :return: The response from the service
    """

    # Initialize the context
    context = ""

    # Send a post request to the Tf-Idf service and get the response
    logger.info(f"Sending a post request to the Tf-Idf service with query: {query}")
    tf_idf_response = requests.post(TF_IDF_URL, params={"query": query})

    # Check the status code and get the response
    if tf_idf_response.status_code == 200:
        # Get the response in JSON
        response = tf_idf_response.json()

        for i in range(len(response)):
            if response[i][1] >= THRESHOLD:
                # Append the relevant information to the context
                logger.info(f"Appending relevant information to the context")
                context += response[i][0] + ". \n"

        return context
    else:
        response = f"Error occurred when processing the request to url {TF_IDF_URL}"

        return response



if __name__ == "__main__":

    res = get_response_tf_idf("tell me about india?")

    print(res)
