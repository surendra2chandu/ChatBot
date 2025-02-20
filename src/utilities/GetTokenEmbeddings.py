# Importing required libraries
from fastapi import HTTPException
from src import logger
from src.utilities.EmbeddingUtility import EmbeddingUtility


class GetTokenEmbeddings:
    def __init__(self):
        """
        This function initializes the GetTokenEmbeddings class.
        """

        # Get the model
        self.model = EmbeddingUtility().get_model()


    def tokenize_and_embed(self, text):
        """
        Tokenizes the text and generates embeddings, handling long texts by splitting them.
        :param text: The text to tokenize.
        :return: The tokens and embeddings.
        """
        try:
            logger.info("Tokenizing text at word level...")
            tokens = text.split()  # Simple word-level tokenization

            logger.info("Generating embeddings for individual tokens...")
            token_embeddings = self.model.embed_documents(tokens)

            return tokens, token_embeddings
        except Exception as e:
            logger.error(f"Error during token embedding: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during token embedding: {e}")

