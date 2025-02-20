# Importing required libraries
from fastapi import HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src import logger
from src.conf.Configurations import model_path
from src.utilities.PDFDataExtractor import PDFDataExtractor


class GetTokenEmbeddings:
    def __init__(self):
        """
        This function initializes the GetTokenEmbeddings class.
        """
        # Initialize the embedding model using LangChain's HuggingFace wrapper
        self.embedder = HuggingFaceEmbeddings(model_name=model_path)

        # Max token limit for the model (to be adjusted based on requirements)
        self.max_token_length = 128

    def tokenize_and_embed(self, text):
        """
        Tokenizes the text and generates embeddings, handling long texts by splitting them.
        :param text: The text to tokenize.
        :return: The tokens and embeddings.
        """
        try:
            logger.info("Splitting text into manageable chunks...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.max_token_length, chunk_overlap=32
            )
            text_chunks = text_splitter.split_text(text)
        except Exception as e:
            logger.error(f"Error during text splitting: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during text splitting: {e}")

        try:
            logger.info("Generating embeddings for text chunks...")
            embeddings = self.embedder.embed_documents(text_chunks)
            return text_chunks, embeddings
        except Exception as e:
            logger.error(f"Error during embedding generation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during embedding generation: {e}")


if __name__ == "__main__":


    text = PDFDataExtractor().extract_text("C:/Docs/sample.pdf")
    # Initialize the GetTokenEmbeddings class and tokenize the text
    token_embedder = GetTokenEmbeddings().tokenize_and_embed(text)

    # Print the tokens and embeddings
    print(token_embedder)
