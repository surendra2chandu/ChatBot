# Import the required modules
from src.conf.Configurations import db_config, logger
import psycopg2
from src.utilities import OllamaServiceManager


class TextSummarizer:
    def __init__(self):
        """
        Initializes the TextSummarizer class
        """
        self.logger = logger

        # Connect to PostgreSQL
        self.logger.info("Connecting to PostgreSQL.")
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def summarize(self, doc_id):
        """
        Summarizes the document text for the given doc_id.
        :param doc_id: The document ID for which to summarize the text.
        :return: The summarized text.
        """

        # Fetch all chunks for the given doc_id
        self.logger.info(f"Extracting document text for doc_id: {doc_id}")
        self.cursor.execute("""
            SELECT chunk
            FROM document_chunks
            WHERE doc_id = %s
            ORDER BY chunk_id ASC
        """, (doc_id,))

        # List of tuples like [(chunk1,), (chunk2,), ...]
        chunks = self.cursor.fetchall()  # List of tuples like [(chunk1,), (chunk2,), ...]

        if not chunks:
            self.logger.warning(f"No chunks found for doc_id: {doc_id}")
            return ""

        # Convert list of tuples to a single string
        document_text = " ".join(chunk[0] for chunk in chunks)

        # Summarize the document text using the Ollama service
        self.logger.info("Summarizing the document text using the Ollama service.")
        summary = OllamaServiceManager.summarize_text(document_text)

        # Close the cursor and connection
        self.logger.info("Closing the cursor and connection.")
        self.cursor.close()
        self.conn.close()

        # Return the summary
        return summary



if __name__ == "__main__":
    # Run summarization
    TextSummarizer().summarize("doc1")
