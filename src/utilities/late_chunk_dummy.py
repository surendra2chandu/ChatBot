# Importing required libraries
import numpy as np
from fastapi import HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sklearn.metrics.pairwise import cosine_similarity
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
        self.text_chunks = []
        self.embeddings = []

    def latechunking(self, text_chunks, embeddings):
        """
        Applies late chunking on embeddings after initial embedding generation, using mean pooling.
        :param text_chunks: The text chunks generated.
        :param embeddings: The embeddings corresponding to the text chunks.
        :return: Re-chunked embeddings with mean pooling.
        """
        try:
            logger.info("Applying late chunking with mean pooling to embeddings...")
            late_chunked_embeddings = []
            new_text_chunks = []
            for i in range(0, len(embeddings), 2):  # Example of late chunking
                chunk = embeddings[i:i + 2]
                if len(chunk) > 1:
                    mean_pooled = np.mean(chunk, axis=0)  # Mean pooling over adjacent chunks
                else:
                    mean_pooled = chunk[0]
                late_chunked_embeddings.append(mean_pooled)
                new_text_chunks.append(" ".join(text_chunks[i:i + 2]))
            return new_text_chunks, late_chunked_embeddings
        except Exception as e:
            logger.error(f"Error during late chunking: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during late chunking: {e}")

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
            self.text_chunks = text_splitter.split_text(text)
        except Exception as e:
            logger.error(f"Error during text splitting: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during text splitting: {e}")

        try:
            logger.info("Generating embeddings for text chunks...")
            self.embeddings = self.embedder.embed_documents(self.text_chunks)

            # Apply late chunking with mean pooling
            self.text_chunks, self.embeddings = self.latechunking(self.text_chunks, self.embeddings)
            return self.text_chunks, self.embeddings
        except Exception as e:
            logger.error(f"Error during embedding generation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during embedding generation: {e}")

    def answer_query(self, query):
        """
        Finds the top 3 matching chunks for the given query using cosine similarity.
        :param query: The query to search for in the document.
        :return: The top 3 most relevant text chunks with their similarity scores.
        """
        try:
            logger.info("Embedding the query...")
            query_embedding = self.embedder.embed_documents([query])[0]

            logger.info("Calculating cosine similarity...")
            similarities = cosine_similarity([query_embedding], self.embeddings)[0]

            top_3_indices = np.argsort(similarities)[-3:][::-1]  # Get indices of top 3 matches
            top_3_matches = [(self.text_chunks[i], similarities[i]) for i in top_3_indices]

            return top_3_matches
        except Exception as e:
            logger.error(f"Error during query answering: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during query answering: {e}")


if __name__ == "__main__":
    text = PDFDataExtractor().extract_text("C:/Docs/gopichandnemalipuri_resume.pdf")
    # Initialize the GetTokenEmbeddings class and tokenize the text
    embedder = GetTokenEmbeddings()
    embedder.tokenize_and_embed(text)

    # Example query
    query = "where is gopichand worked in june 2023?"
    top_matches = embedder.answer_query(query)

    # Print the top 3 answers with scores
    for idx, (chunk, score) in enumerate(top_matches):
        print(f"Match {idx + 1}: Score: {score:.4f}\nText: {chunk}\n")
