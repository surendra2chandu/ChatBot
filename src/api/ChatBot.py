# import necessary libraries
from src import logger
from src.conf.Configurations import SEMANTIC_CONFIGURATION
from src.utilities.OllamaServiceManager import process_ollama_request
from src.utilities.ChatBotUtilities import ChatBotUtilities
from src.retrival.Retrival import Retrival

class ChatBot:

    @staticmethod
    def get_response(query, doc_id):
        """
        Function to get response from the LateChunking service
        :param query: The query to be processed
        :param doc_id: The document id
        :return: The response from the service
        """

        # Get the similar documents
        logger.info("Getting the similar documents...")
        similar_documents  = Retrival().get_similar_documents(query, doc_id)

        if similar_documents:

            if SEMANTIC_CONFIGURATION == "BOTH":

                # Get the text from the semantically similar documents and the Tf-Idf similar documents
                logger.info("Getting the text from the semantically similar documents and the Tf-Idf similar documents...")
                context = ChatBotUtilities().get_sematic_similar_documents_text(similar_documents) + ChatBotUtilities().get_tf_idf_similar_documents_text(similer_documents)

            elif SEMANTIC_CONFIGURATION == "Tf_Idf":

                # Get the text from the Tf-Idf similer documents
                logger.info("Getting the text from the Tf-Idf similer documents...")
                context = ChatBotUtilities().get_tf_idf_similer_documents_text(similer_documents)

            else:

                # Get the text from the semantically similer documents
                logger.info("Getting the text from the semantically similer documents...")
                context = ChatBotUtilities().get_sematic_similer_documents_text(similer_documents)

            if context:
                # Process the response with the Ollama model
                logger.info("Processing the response with the Ollama model")
                response = process_ollama_request(context, query)
            else:
                response = "No relevant information found in the database."

            return response

        else:
            return "Error occurred while processing the request "


if __name__ == "__main__":

    res = ChatBot.get_response("where is gopichand worked in june 2023?", "doc7")

    print(res)
