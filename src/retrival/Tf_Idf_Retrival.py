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
    sample_query="makes visible to leadership all product support aspects of the program and should describe all stakeholders roles and responsibilities to include any organization with delegated sustain ment responsibilities such as other services product groups andor support providers 12 the lcsp evolves into an execution plan to describe the manner in which life cycle sustainment requirements are acquired applie d managed assessed measured and reported after system fielding by milestone ms c the lcsp should detail how the program will meet readiness targets sustain system performance capability threshold criteria comply with title 10 u nited states code usc 2337 life cycle management and product support 10 usc 2464 core logistics capabilities and 10 usc 2466 limitations on"
    top_docs = TfIdfRetrival().retrieve_relevant_docs(sample_query, "doc1")

    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")
