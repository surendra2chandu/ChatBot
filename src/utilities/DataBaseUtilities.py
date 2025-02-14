# Importing the required libraries
from src.conf.Configurations import logger, db_config, NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL
import psycopg2


class DataBaseUtility:
    def __init__(self):
        """                                                        vvvv
        This function initializes the DataBaseUtility class with the specified database configuration.
        """

        # Set the database configuration
        self.db_config = db_config

        # Connect to the database
        logger.info("Connecting to the database...")
        self.conn = psycopg2.connect(**self.db_config)

        # Create a cursor object
        self.cursor = self.conn.cursor()


    # Function to store chunks in the database
    def store_chunks_in_db(self, chunks, doc_name, doc_type):
        """
        This function stores the chunks in the database.
        :param chunks: The chunks to store.
        :param doc_name: The name of the document.
        :param doc_type: The type of the document.
        :return: None
        """


        # # Drop the table if it exists
        # logger.info("Dropping the table if it exists...")
        # self.cursor.execute("DROP TABLE IF EXISTS document_chunks;")

        # Create the table if it doesn't exist (Using pgvector's vector type for embeddings)
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS document_chunks (
                        doc_id SERIAL PRIMARY KEY,
                        doc_name TEXT,
                        doc_type CHAR(1),
                        chunk TEXT,
                        embedding vector  
                    );
                """)

        # Insert the data
        for chunk_text, chunk_embedding in chunks:
            chunk_embedding_list = chunk_embedding.astype(float).tolist()  # Convert numpy array to list of floats

            self.cursor.execute(
                """
                INSERT INTO document_chunks (doc_name, doc_type, chunk, embedding)
                VALUES (%s, %s, %s, %s::vector)  -- Cast the embedding to the vector type
                """,
                (doc_name, doc_type,  chunk_text, chunk_embedding_list),
            )

        # Commit the changes
        logger.info("Committing the changes...")
        self.conn.commit()


    def fetch_similar_text(self, query_embedding):
        """
        This function retrieves all matches for the query sorted by similarity in descending order.
        :param query_embedding: The embedding of the query.
        :return: The results sorted by similarity in descending order.
        """


        # Retrieve all matches sorted by similarity in descending order
        logger.info("Retrieving all matches for the query...")
        self.cursor.execute(
            """
            SELECT chunk, 1 - (embedding <=> %s::vector) AS similarity
            FROM document_chunks
            ORDER BY similarity DESC
            LIMIT %s;
            """,
            (query_embedding.tolist(), NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL)
        )

        # Fetch the results
        logger.info("Fetching the results...")
        results = self.cursor.fetchall()

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()

        # Return the results
        return results



    def extract_doc_content(self, doc_type = 'D'):
        """
        This function retrieves all the web content from the database.
        :return: The doc content.
        """
        # Retrieve all web content
        logger.info("Retrieving all doc content...")
        self.cursor.execute(
            """
            SELECT chunk
            FROM document_chunks
            WHERE doc_type = 'W';
            """
        )

        # Fetch the results
        logger.info("Fetching the results...")
        results = self.cursor.fetchall()

        # Convert the results to a list
        chunks = [row[0] for row in results]

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()

        # Return the results
        return chunks


    def document_exists(self, file_name):
        """
        Checks if a document with the given name already exists in the database.
        :param file_name: Name of the document to check.
        :return: True if document exists, otherwise False.
        """
        self.cursor.execute("SELECT 1 FROM document_chunks WHERE doc_name = %s", (file_name,))
        return self.cursor.fetchone() is not None


    def close(self):
        """
        This function closes the cursor and connection.
        :return: None
        """

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()


