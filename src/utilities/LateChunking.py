# Importing required libraries
from src import logger
from src.conf.Configurations import CHUNK_SIZE
from fastapi import HTTPException
import numpy as np


class LateChunking:
    def __init__(self):
        """
        This function initializes the LateChunking class.
        """

    # Late chunking function
    def late_chunk(self, tokens, embeddings):
        """
        This function chunks the tokens and embeddings.
        :param tokens: The tokens.
        :param embeddings: The embeddings.
        :return:
        """

        # Initialize the list to store mean embeddings and text chunks
        chunks = []

        try:
            logger.info("Applying late chunking with mean pooling...")

            for i in range(0, len(tokens), CHUNK_SIZE):
                chunk_tokens = tokens[i: i + CHUNK_SIZE]
                chunk_embeddings = embeddings[i: i + CHUNK_SIZE]

                if chunk_embeddings:
                    mean_pooled_embedding = np.mean(chunk_embeddings, axis=0)  # Mean pooling
                    chunks.append((" ".join(chunk_tokens), mean_pooled_embedding))

            return chunks
        except Exception as e:
            logger.error(f"Error during late chunking: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during late chunking: {e}")
