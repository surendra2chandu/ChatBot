# Importing required libraries
from fastapi import HTTPException
from src import logger
from src.utilities.EmbeddingUtility import EmbeddingUtility
# to-do : use langchain modules to get the embeddings
import torch


class GetTokenEmbeddings:
    def __init__(self):
        """
        This function initializes the GetTokenEmbeddings class.
        """
        # Get the tokenizer
        self.tokenizer = EmbeddingUtility().get_tokenizer()

        # Get the model
        self.model = EmbeddingUtility().get_model()

        # Max token limit for the model
        # to-do : get the max token limit from the model  (snow flake)
        self.max_token_length = 512

    def tokenize_and_embed(self, text):
        """
        Tokenizes the text and generates embeddings, handling long texts by splitting them.
        :param text: The text to tokenize.
        :return: The tokens and embeddings.
        """
        try:
            # Tokenize the text
            logger.info("Tokenizing the text...")
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=False,  # Disable truncation to handle splitting manually
                add_special_tokens=False,
            )
            input_ids = inputs["input_ids"][0]

            # Split input IDs into chunks of max_token_length
            logger.info("Splitting text into manageable chunks...")
            chunks = [
                input_ids[i : i + self.max_token_length]
                for i in range(0, len(input_ids), self.max_token_length)
            ]
        except Exception as e:
            logger.error(f"Error during tokenization: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during tokenization of the text: {e}")

        # Initialize lists to store tokens and embeddings
        all_tokens = []
        all_embeddings = []

        try:
            # Process each chunk
            for chunk in chunks:
                logger.info("Processing a chunk of tokens...")
                chunk_inputs = {"input_ids": chunk.unsqueeze(0)}

                with torch.no_grad():
                    outputs = self.model(**chunk_inputs)
                    embeddings = outputs.last_hidden_state

                # Convert input IDs to tokens
                tokens = self.tokenizer.convert_ids_to_tokens(chunk)
                all_tokens.extend(tokens)
                all_embeddings.append(embeddings[0])

            return all_tokens, torch.cat(all_embeddings, dim=0)
        except Exception as e:
            logger.error(f"Error during tokenization and embedding: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during tokenization and embedding: {e}")