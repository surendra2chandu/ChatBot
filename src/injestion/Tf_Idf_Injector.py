# Import necessary libraries
import psycopg2
from sklearn.feature_extraction.text import TfidfVectorizer
from src.conf.Configurations import db_config, logger
from src.utilities.DataBaseUtilities import DataBaseUtility


class TfIdfInjector:
    def __init__(self):
        """
        Initialize the TF-IDF injector.
        """

        # Fetch document content from database
        logger.info("Fetching document content...")
        self.corpus = DataBaseUtility().extract_doc_content()

        # Compute TF-IDF
        logger.info("Computing TF-IDF...")
        self.vectorizer = TfidfVectorizer()

        # Fit the vectorizer
        logger.info("Fitting the vectorizer...")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus).toarray()


    def store_tfidf_data(self):
        """
        Store the TF-IDF data in the database.
        :return: None
        """

        # Connect to PostgreSQL
        logger.info("Connecting to PostgreSQL...")
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Drop the table if it exists
        logger.info("Dropping the table if it exists...")
        cursor.execute("DROP TABLE IF EXISTS documents;")

        # Create the table
        logger.info("Creating the table...")
        cursor.execute("""
            CREATE TABLE documents (
                id SERIAL PRIMARY KEY,
                document_text TEXT,
                tfidf_vector vector
            )
        """)

        # Insert each document and its vector
        logger.info("Inserting documents and their vectors...")
        for doc, vec in zip(self.corpus, self.tfidf_matrix):
            cursor.execute(
                "INSERT INTO documents (document_text, tfidf_vector) VALUES (%s, %s::vector)",
                (doc, vec.tolist())  # Convert NumPy array to list for PostgreSQL
            )

        # Commit and close
        logger.info("Committing and closing...")
        conn.commit()
        cursor.close()
        conn.close()

    def get_vectorizer(self):
        """
        Get the vectorizer object.
        :return: The vectorizer object.
        """

        # Return the vectorizer object
        return self.vectorizer



# Run ingestion
if __name__ == "__main__":
    TfIdfInjector().store_tfidf_data()
