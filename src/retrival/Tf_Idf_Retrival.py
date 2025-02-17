# Import necessary libraries , classes and functions
from src import logger
from src.injestion.Tf_Idf_Injector import TfIdfInjector
from src.database_utilities.TfIdf_Table import TfIdfTable
from fastapi import HTTPException


class TfIdfRetrival:

    @staticmethod
    def retrieve_relevant_docs(query: str, doc_id: str):
        """
        Extracts documents similar to the query using TF-IDF.
        :param query: The query to search for.
        :param doc_id: The document id to search for.
        :return: The list of tuples containing the document text and similarity score.
        """
        try:
            # Initialize the TF-IDF injector
            logger.info("Initializing the TF-IDF injector.")
            vectorizer = TfIdfInjector().get_vectorizer()

            # Transform query to TF-IDF vector
            logger.info("Transforming the query to a TF-IDF vector.")
            query_vec = vectorizer.transform([query]).toarray()[0]
        except Exception as e:
            logger.info(f"Error in transforming the query to a TF-IDF vector: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during transformation: {e}")

        # Query most similar documents using SQL cosine similarity
        logger.info("Querying the most similar documents using SQL cosine similarity.")
        results = TfIdfTable().get_similar_documents(doc_id, query_vec)

        return results


# Run retrieval
if __name__ == "__main__":
    sample_query="NEMALIPURI GOPICHAND 7993269669 nvgopichand68776gmail com LinkedIn wwwlinkedincominnemalipuri gopichand 7bb231222 DATA SCIENTIST AND MACHINE LEARNING ENGINEER Innovative and detail oriented Junior Data Scientist and Machine Learning Engineer with a solid foundation in data science machine learning and artificial intelligence Adept at developing and i mplementing data driven solutions to drive business insights and optimize processes Skilled in designing and executing machine learning models performing data analysis and automating workflows using advanced technologies Demonstrates strong analytical abilities and problem solving skills with"
    top_docs = TfIdfRetrival().retrieve_relevant_docs(sample_query, "doc7")

    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")
