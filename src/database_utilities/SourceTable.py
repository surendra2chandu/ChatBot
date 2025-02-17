# Importing the required libraries
from src import logger
from src.conf.Configurations import db_config, DOC_TYPE_FOR_PDF
import psycopg2


class SourceTable:
    def __init__(self):
        """
        This function initializes the DataBaseUtility class with the specified database configuration.
        """

        # Set the database configuration
        self.db_config = db_config

        # Connect to the database
        logger.info("Connecting to the database...")
        self.conn = psycopg2.connect(**self.db_config)

        # Create a cursor object
        self.cursor = self.conn.cursor()

    def store_doc_info(self, doc_name):
        """
        This function creates the source table in the database.
        :return: None
        """

        # Drop the table if it exists
        # logger.info("Dropping the table if it exists...")
        # self.cursor.execute("DROP TABLE IF EXISTS source_table;")

        # Create the table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS source_table (
                doc_id TEXT,  -- Unique identifier for each document
                doc_name TEXT,
                doc_type CHAR(1),
            );
        """)

        # Get the count of unique documents already stored
        self.cursor.execute("SELECT COUNT(DISTINCT doc_name) FROM document_chunks;")
        doc_count = self.cursor.fetchone()[0]  # Get the count of unique document names

        # Assign a unique doc_id
        doc_id = f"doc{doc_count + 1}"  # Generates doc1, doc2, etc.

        # Insert the data
        self.cursor.execute(
            "INSERT INTO source_table (doc_id, doc_name, doc_type) VALUES (%s, %s, %s);",
            (doc_id, doc_name, DOC_TYPE_FOR_PDF)
        )

        # Commit the transaction and close the connection
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        logger.info("Document information stored successfully.")

        return doc_id


    def document_exists(self, file_name):
        """
        Checks if a document with the given name already exists in the database.
        :param file_name: Name of the document to check.
        :return: True if document exists, otherwise False.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM document_chunks WHERE doc_name = %s", (file_name,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            if "does not exist" in str(e):  # Adjust based on the actual DB error message
                return False




