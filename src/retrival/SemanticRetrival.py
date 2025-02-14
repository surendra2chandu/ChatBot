# Importing required libraries
from src.conf.Configurations import logger
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
from src.utilities.DataBaseUtilities import DataBaseUtility


class SemanticRetrival:
    @staticmethod
    def retrieve_relevant_docs( query):
        """
        This function retrieves relevant text based on the query.
        :param query: The query to search for.
        :return: List of tuples containing the text chunk and similarity score.
        """

        # Tokenize and embed the query
        logger.info("Tokenizing and embedding the query...")
        res = GetTokenEmbeddings().tokenize_and_embed(query)

        # Get the mean of the embeddings
        logger.info("Getting the mean of the embeddings...")
        query_embedding = res[1].mean(dim=0).numpy()

        # Fetch similar text from the database
        logger.info("Fetching similar text from the database...")
        result = DataBaseUtility().fetch_similar_text(query_embedding)

        return result

if __name__ == "__main__":
    # Sample query
    sample_query = "Who are the customers impacted by the upcoming satellite change for the AFN TV programming package in the Pacific region?"

    # Retrieve relevant text
    results = SemanticRetrival().retrieve_relevant_docs(sample_query)

    for chunk, similarity in results:
        print(f"Chunk: {chunk}\nSimilarity: {similarity}\n")



