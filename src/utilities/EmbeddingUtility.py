# Importing required libraries
# to-do : use langchain transformers modules to get the embeddings
from src import logger
from src.conf.Configurations import model_path
from fastapi import HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings



class EmbeddingUtility:
    def __init__(self):
        """
        This function initializes the LateChunking class with the specified model path.
        """

        # Set the model name
        self.model_name = model_path

        try:

            # Load the model
            logger.info(f"Loading model from {self.model_name}...")
            self.model = HuggingFaceEmbeddings(model_name=model_path)
        except Exception as e:
            # Log the error
            logger.error(f"Error during model loading: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during model loading: {e}")

    def get_model(self):
        """
        This function returns the model.
        :return: Model
        """

        # Return the model
        return self.model


