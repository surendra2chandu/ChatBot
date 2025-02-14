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
        This function stores the chunks in the database with a unique doc_id.
        :param chunks: The chunks to store.
        :param doc_name: The name of the document.
        :param doc_type: The type of the document.
        :return: None
        """

        # Drop the table if it exists
        # logger.info("Dropping the table if it exists...")
        # self.cursor.execute("DROP TABLE IF EXISTS document_chunks;")

        # Create the table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                doc_id TEXT,  -- Unique identifier for each document
                doc_name TEXT,
                doc_type CHAR(1),
                chunk_id SERIAL PRIMARY KEY,  -- Auto-incrementing chunk ID
                chunk TEXT,
                embedding vector  
            );
        """)

        # Get the count of unique documents already stored
        self.cursor.execute("SELECT COUNT(DISTINCT doc_name) FROM document_chunks;")
        doc_count = self.cursor.fetchone()[0]  # Get the count of unique document names

        # Assign a unique doc_id
        doc_id = f"doc{doc_count + 1}"  # Generates doc1, doc2, etc.

        # Insert the data
        for chunk_text, chunk_embedding in chunks:
            chunk_embedding_list = chunk_embedding.astype(float).tolist()  # Convert numpy array to list of floats

            self.cursor.execute(
                """
                INSERT INTO document_chunks (doc_id, doc_name, doc_type, chunk, embedding)
                VALUES (%s, %s, %s, %s, %s::vector)
                """,
                (doc_id, doc_name, doc_type, chunk_text, chunk_embedding_list),
            )

        # Commit the changes
        logger.info(f"Committing the changes for {doc_name} with doc_id {doc_id}...")
        self.conn.commit()


    def fetch_similar_text(self, query_embedding, doc_id):
        """
        This function retrieves all matches for the query sorted by similarity in descending order.
        :param query_embedding: The embedding of the query.
        :param doc_id: The document ID to exclude from the search.
        :return: The results sorted by similarity in descending order.
        """


        # Retrieve all matches sorted by similarity in descending order
        logger.info("Retrieving all matches for the query...")
        self.cursor.execute(
            """
            SELECT chunk, 1 - (embedding <=> %s::vector) AS similarity
            FROM document_chunks Where doc_id = %s
            ORDER BY similarity DESC
            LIMIT %s;
            """,
            (query_embedding.tolist(), doc_id, NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL)
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

    def extract_doc_chunks(self):
        """
        Fetch document chunks and metadata from the database.
        :return: List of dictionaries containing doc_id, doc_name, chunk_id, and chunk.
        """
        try:
            # Fetch relevant columns
            query = """
                SELECT doc_id, doc_name, chunk_id, chunk 
                FROM document_chunks;
            """
            logger.info("Executing query to fetch document chunks...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert list of tuples into list of dictionaries
            columns = ["doc_id", "doc_name", "chunk_id", "chunk"]
            documents = [dict(zip(columns, row)) for row in rows]

            return documents

        except Exception as e:
            logger.error(f"Error fetching document chunks: {e}")
            return []

        finally:
            self.cursor.close()
            self.conn.close()

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

    def close(self):
        """
        This function closes the cursor and connection.
        :return: None
        """

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()


