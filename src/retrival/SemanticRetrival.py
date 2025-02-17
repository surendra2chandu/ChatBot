# Importing required libraries
from src import logger
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
from src.database_utilities.Semantic_Table import SemanticTable
from fastapi import HTTPException


class SemanticRetrival:
    @staticmethod
    def retrieve_relevant_docs( query, doc_id):
        """
        This function retrieves relevant text based on the query.
        :param query: The query to search for.
        :param doc_id: The document id to exclude from the search.
        :return: List of tuples containing the text chunk and similarity score.
        """

        # Tokenize and embed the query
        logger.info("Tokenizing and embedding the query...")
        res = GetTokenEmbeddings().tokenize_and_embed(query)

        try:
            # Get the mean of the embeddings
            logger.info("Getting the mean of the embeddings...")
            query_embedding = res[1].mean(dim=0).numpy()
        except Exception as e:
            logger.error(f"Error in getting the mean of the embeddings: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during mean embedding: {e}")

        # Fetch similar text from the database
        logger.info("Fetching similar text from the database...")
        result = SemanticTable().fetch_similar_text(query_embedding, doc_id)

        return result

if __name__ == "__main__":
    # Sample query
    sample_query = "Who are the customers impacted by the upcoming satellite change for the AFN TV programming package in the Pacific region?"

    # Retrieve relevant text
    results = SemanticRetrival().retrieve_relevant_docs(sample_query, "doc4")

    for chunk, similarity in results:
        print(f"Chunk: {chunk}\nSimilarity: {similarity}\n")



