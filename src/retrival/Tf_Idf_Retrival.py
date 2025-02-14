# Import necessary libraries , classes and functions
import psycopg2
from src.conf.Configurations import db_config, NUMBER_OF_MATCHES_FOR_TF_IDF, logger
from src.injestion.Tf_Idf_Injector import TfIdfInjector

class TfIdfRetrival:

    @staticmethod
    def retrieve_relevant_docs(query: str, doc_id: str):
        """
        Extracts documents similar to the query using TF-IDF.
        :param query: The query to search for.
        :param doc_id: The document id to search for.
        :return: The list of tuples containing the document text and similarity score.
        """

        # Initialize the TF-IDF injector
        logger.info("Initializing the TF-IDF injector.")
        vectorizer = TfIdfInjector().get_vectorizer()

        # Transform query to TF-IDF vector
        logger.info("Transforming the query to a TF-IDF vector.")
        query_vec = vectorizer.transform([query]).toarray()[0]

        # Connect to PostgreSQL
        logger.info("Connecting to PostgreSQL.")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Query most similar documents using SQL cosine similarity
        logger.info("Querying the most similar documents using SQL cosine similarity.")
        cursor.execute("""
            SELECT chunk, 1 - (tfidf_vector <=> %s::vector) AS similarity
            FROM tf_idf_documents Where doc_id = %s
            ORDER BY similarity DESC  -- Lower distance means higher similarity
            LIMIT %s
        """, (query_vec.tolist(),doc_id,  NUMBER_OF_MATCHES_FOR_TF_IDF))

        # Fetch results
        logger.info("Fetching results.")
        results = cursor.fetchall()

        # Close the cursor and connection
        logger.info("Closing the cursor and connection.")
        cursor.close()
        conn.close()

        return results


# Run retrieval
if __name__ == "__main__":
    sample_query="this document explores the importance of effective communication in project management it highlights various strategies that enhance team collaboration stakeholder engagement and overall project success modi was born and raised in vadnagar in nor theastern gujarat where he completed his secondary education he was introduced to the rss at the age of eight this document explores the importance of effective communication in project management it highlights various strategies that enhance team collaboration stakeholder engagement and overall project success modi was born and raised in vadnagar in nor theastern gujarat where he completed his secondary education he was introduced to the rss at the age of eight"
    top_docs = TfIdfRetrival().retrieve_relevant_docs(sample_query, "doc6")

    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")
