# Importing required libraries
# Updated to use LangChain's embedding models
from src import logger
from langchain_community.embeddings import HuggingFaceEmbeddings
from src.conf.Configurations import model_path
from fastapi import HTTPException


class EmbeddingUtility:
    def __init__(self):
        """
        This function initializes the EmbeddingUtility class with the specified model path.
        """

        # Set the model name
        self.model_name = model_path

        try:
            # Load the embedding model
            logger.info(f"Loading embedding model from {self.model_name}...")
            self.embeddings = HuggingFaceEmbeddings(model_name=self.model_name)
        except Exception as e:
            # Log the error
            logger.error(f"Error during model loading: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during model loading: {e}")

    def get_embeddings(self):
        """
        This function returns the embedding model.
        :return: Embedding model
        """
        return self.embeddings
