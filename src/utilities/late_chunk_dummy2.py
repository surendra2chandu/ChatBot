# Importing required libraries
import numpy as np
from fastapi import HTTPException
from langchain_community.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
from src import logger
from src.conf.Configurations import model_path
from src.utilities.PDFDataExtractor import PDFDataExtractor
from src.utilities.OllamaServiceManager import process_ollama_request


class GetTokenEmbeddings:
    def __init__(self):
        """
        Initializes the GetTokenEmbeddings class.
        """
        # Initialize the embedding model using LangChain's HuggingFace wrapper
        self.embedder = HuggingFaceEmbeddings(model_name=model_path)

        # Define token and chunking parameters
        self.chunk_size = 128
        self.chunk_overlap = 32
        self.tokens = []
        self.token_embeddings = []
        self.text_chunks = []
        self.chunk_embeddings = []

    def tokenize_and_embed_tokens(self, text):
        """
        Tokenizes the text into words and generates embeddings for each token.
        :param text: The text to tokenize.
        :return: A list of tokens and their corresponding embeddings.
        """


    def latechunking(self):
        """
        Groups token embeddings into chunks of 128 tokens with 32-token overlap using mean pooling.
        :return: Late-chunked text segments and their embeddings.
        """
        try:
            logger.info("Applying late chunking with mean pooling...")

            for i in range(0, len(self.tokens), self.chunk_size - self.chunk_overlap):
                chunk_tokens = self.tokens[i: i + self.chunk_size]
                chunk_embeddings = self.token_embeddings[i: i + self.chunk_size]

                if chunk_embeddings:
                    mean_pooled_embedding = np.mean(chunk_embeddings, axis=0)  # Mean pooling
                    self.chunk_embeddings.append(mean_pooled_embedding)
                    self.text_chunks.append(" ".join(chunk_tokens))

            return self.text_chunks, self.chunk_embeddings
        except Exception as e:
            logger.error(f"Error during late chunking: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during late chunking: {e}")

    def answer_query(self, query):
        """
        Finds the top 3 matching chunks for the given query using cosine similarity.
        :param query: The query to search for in the document.
        :return: The top 3 most relevant text chunks with their similarity scores.
        """
        try:
            logger.info("Embedding the query at token level...")
            query_tokens = query.split()
            query_embeddings = self.embedder.embed_documents(query_tokens)

            logger.info("Applying mean pooling for query embedding...")
            query_embedding = np.mean(query_embeddings, axis=0)  # Mean pooling for query

            logger.info("Calculating cosine similarity...")
            similarities = cosine_similarity([query_embedding], self.chunk_embeddings)[0]

            top_3_indices = np.argsort(similarities)[-3:][::-1]  # Get indices of top 3 matches
            top_3_matches = [(self.text_chunks[i], similarities[i]) for i in top_3_indices]

            return top_3_matches
        except Exception as e:
            logger.error(f"Error during query answering: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during query answering: {e}")


if __name__ == "__main__":
    text = PDFDataExtractor().extract_text("C:/Docs/gopichandnemalipuri_resume.pdf")

    # Initialize the GetTokenEmbeddings class
    embedder = GetTokenEmbeddings()

    # Perform token-level embedding and late chunking
    embedder.tokenize_and_embed_tokens(text)
    embedder.latechunking()

    # Example query
    query = "Where gopichand worked in june 2023?"

    # query = "Tell me the companies gopichand worked in his career?"
    top_matches = embedder.answer_query(query)
    context = ""
    # Print the top 3 matches with similarity scores
    for idx, (chunk, score) in enumerate(top_matches):
        print(f"Match {idx + 1}: Score: {score:.4f}\nText: {chunk}\n")

        context += chunk

    res = process_ollama_request(context, query)

    print(res)


