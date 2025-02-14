# Importing required libraries
from transformers import AutoTokenizer, AutoModel
from src.conf.Configurations import logger, model_path


class EmbeddingUtility:
    def __init__(self):
        """
        This function initializes the LateChunking class with the specified model path.
        """

        # Set the model name
        self.model_name = model_path

        # Load the tokenizer
        logger.info(f"Loading tokenizer from {self.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # Load the model
        logger.info(f"Loading model from {self.model_name}...")
        self.model = AutoModel.from_pretrained(self.model_name)


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


