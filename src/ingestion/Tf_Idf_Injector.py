# Import necessary libraries
from src import logger
# to-do : use langchain module
from sklearn.feature_extraction.text import TfidfVectorizer
from src.database_utilities.TfIdf_Table import TfIdfTable
from fastapi import HTTPException


class TfIdfInjector:
    def __init__(self):
        """
        Initialize the TF-IDF injector.
        """

        # Fetch document content from database
        logger.info("Fetching document content...")
        self.corpus = TfIdfTable().extract_doc_chunks()  # Fetch all columns

        # Compute TF-IDF
        try:
            logger.info("Computing TF-IDF...")
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus).toarray()

        except Exception as e:
            logger.error(f"Error during TF-IDF computation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during TF-IDF computation: {e}")

    def store_tfidf_data(self):
        """
        Store the TF-IDF data in the database.
        :return: None
        """

        TfIdfTable().insert_tf_idf_vector(self.corpus, self.tfidf_matrix)

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
