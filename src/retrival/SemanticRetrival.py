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
    sample_query = "NEMALIPURI GOPICHAND 7993269669 nvgopichand68776gmail com LinkedIn wwwlinkedincominnemalipuri gopichand 7bb231222 DATA SCIENTIST AND MACHINE LEARNING ENGINEER Innovative and detail oriented Junior Data Scientist and Machine Learning Engineer with a solid foundation in data science machine learning and artificial intelligence Adept at developing and i mplementing data driven solutions to drive business insights and optimize processes Skilled in designing and executing machine learning models performing data analysis and automating workflows using advanced technologies Demonstrates strong analytical abilities and problem solving skills with"
    # Retrieve relevant text
    results = SemanticRetrival().retrieve_relevant_docs(sample_query, "doc7")

    for chunk, similarity in results:
        print(f"Chunk: {chunk}\nSimilarity: {similarity}\n")



