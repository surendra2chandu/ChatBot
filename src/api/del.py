# Importing required libraries
from src import logger
from src.conf.Configurations import model_path
from fastapi import HTTPException
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama.llms import OllamaLLM



class GetTokenEmbeddings:
    def __init__(self):
        """
        This function initializes the GetTokenEmbeddings class.
        """

        # Get the model
        self.model = OllamaLLM(base_url="http://127.0.0.1:11434", model="all-minilm")


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
            token_embeddings = self.model.embeddings(tokens)

            return tokens, token_embeddings
        except Exception as e:
            logger.error(f"Error during token embedding: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during token embedding: {e}")


if __name__ == "__main__":
    # Test the GetTokenEmbeddings class
    text = "This is a test sentence."
    embeddings = GetTokenEmbeddings().tokenize_and_embed(text)
    print(embeddings)

