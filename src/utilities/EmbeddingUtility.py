# Importing required libraries
# to-do : use langchain transformers modules to get the embeddings
from src import logger
from transformers import AutoTokenizer, AutoModel
from src.conf.Configurations import model_path
from fastapi import HTTPException


class EmbeddingUtility:
    def __init__(self):
        """
        This function initializes the LateChunking class with the specified model path.
        """

        # Set the model name
        self.model_name = model_path

        try:
            # Load the tokenizer
            logger.info(f"Loading tokenizer from {self.model_name}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

            # Load the model
            logger.info(f"Loading model from {self.model_name}...")
            self.model = AutoModel.from_pretrained(self.model_name)
        except Exception as e:
            # Log the error
            logger.error(f"Error during model loading: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during model loading: {e}")


    def get_tokenizer(self):
        """
        This function returns the tokenizer.
        :return: Tokenizer
        """

        # Return the tokenizer
        return self.tokenizer

    def get_model(self):
        """
        This function returns the model.
        :return: Model
        """

        # Return the model
        return self.model


