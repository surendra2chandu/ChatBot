# Import necessary libraries , classes and functions
import psycopg2
from src.conf.Configurations import db_config, NUMBER_OF_MATCHES_FOR_TF_IDF, logger
from src.injestion.Tf_Idf_Injector import TfIdfInjector

class TfIdfRetrival:

    @staticmethod
    def retrieve_relevant_docs(query: str):
        """
        Extracts documents similar to the query using TF-IDF.
        :param query: The query to search for.
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
            SELECT document_text, 1 - (tfidf_vector <=> %s::vector) AS similarity
            FROM documents
            ORDER BY similarity DESC  -- Lower distance means higher similarity
            LIMIT %s
        """, (query_vec.tolist(), NUMBER_OF_MATCHES_FOR_TF_IDF))

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
    sample_query="air force lifecycle management center, wright - patterson air force base, ohio, is the contracting activity. raytheon technologies corp., pratt & whitney engines, east hartford, connecticut, has been awarded an indefinite - delivery / indefinite - quantity modification ( p00006 ) with a program ceiling of $ 3, 500, 000, 000 to previously awarded contract fa8626 - 22 - d - 0002 for technology maturation and risk reduction services. the work includes design, analysis, rig testing, prototype engine build and testing, and weapon system integration. the contract modification is for the execution of the prototype phase of the next generation"
    top_docs = TfIdfRetrival().retrieve_relevant_docs(sample_query)

    print(top_docs)

    print("\nTop similar documents:")
    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")
