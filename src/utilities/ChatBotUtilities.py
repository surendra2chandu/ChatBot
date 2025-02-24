# Import necessary libraries
from src import logger
from src.conf.Configurations import THRESHOLD_FOR_SEMANTIC_RETRIVAL, THRESHOLD_FOR_TF_IDF

class ChatBotUtilities:

    @staticmethod
    def get_sematic_similar_documents_text(similar_documents):
        """
        Function to get the text from the semantically similar documents
        :param similar_documents: The similar documents
        :return: The text from the similar documents
        """

        # Initialize the context
        context = ""

        # Get the text from the semantically similar documents
        logger.info("Getting the text from the semantically similar documents...")
        for doc in similar_documents["semantic_similar_documents"]:
            if doc[1] >= THRESHOLD_FOR_SEMANTIC_RETRIVAL:
                context += doc[0] + " "

        # Return the context
        return context

    @staticmethod
    def get_tf_idf_similar_documents_text(similar_documents):
        """
        Function to get the text from the Tf-Idf similar documents
        :param similar_documents: The similar documents
        :return: The text from the similar documents
        """

        # Initialize the context
        context = ""

        # Get the text from the Tf-Idf similar documents
        logger.info("Getting the text from the Tf-Idf similar documents...")
        for doc in similar_documents["tf_idf_similar_documents"]:
            if doc[1] >= THRESHOLD_FOR_TF_IDF:
                context += doc[0] + " "

        # Return the context
        return context