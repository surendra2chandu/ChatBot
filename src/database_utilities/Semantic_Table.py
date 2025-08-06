# Importing the required libraries
from src import logger
from src.conf.Configurations import  db_config, NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL, DOC_TYPE_FOR_PDF
import psycopg2
from fastapi import HTTPException


class SemanticTable:
    def __init__(self):
        """
        This function initializes the DataBaseUtility class with the specified database configuration.
        """
        try:
            # Set the database configuration
            self.db_config = db_config

            # Connect to the database
            logger.info("Connecting to the database...")
            self.conn = psycopg2.connect(**self.db_config)




            # Create a cursor object
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.error(f"Error during initialization of the database connection: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during database connection: {e}")


    # Function to store chunks in the database
    def store_chunks_in_db(self, chunks, doc_name):
        """
        This function stores the chunks in the database with a unique doc_id.
        :param chunks: The chunks to store.
        :param doc_name: The name of the document.
        :return: None
        """

        # Drop the table if it exists
        # logger.info("Dropping the table if it exists...")
        # self.cursor.execute("DROP TABLE IF EXISTS document_chunks;")

        try:
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

        except Exception as e:
            logger.error(f"Error during table creation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during table creation: {e}")

        try:
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
                    (doc_id, doc_name, DOC_TYPE_FOR_PDF, chunk_text, chunk_embedding_list),
                )

            # Commit the changes
            logger.info(f"Committing the changes for {doc_name} with doc_id {doc_id}...")
            self.conn.commit()

        except Exception as e:
            logger.error(f"Error during insertion of chunks: {e}")
            raise HTTPException(status_code=422, detail=f"An error occurred during insertion of chunks: {e}")


    def fetch_similar_text(self, query_embedding, doc_id):
        """
        This function retrieves all matches for the query sorted by similarity in descending order.
        :param query_embedding: The embedding of the query.
        :param doc_id: The document ID to exclude from the search.
        :return: The results sorted by similarity in descending order.
        """

        try:
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

            # Return the results
            return results

        except Exception as e:
            logger.error(f"Error during retrieval of similar text: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during retrieval of similar text: {e}")

        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection...")
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
        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection...")
            self.cursor.close()
            self.conn.close()

    def get_all_document_ids(self):
        """
        Fetches all document IDs from the database in the order they are stored.
        :return: List of document IDs.
        """
        try:
            # Fetch all document IDs in order
            logger.info("Fetching all document IDs in order...")
            self.cursor.execute("SELECT DISTINCT doc_id FROM document_chunks ORDER BY doc_id;")
            doc_ids = [row[0] for row in self.cursor.fetchall()]  # Extracting IDs from tuples

            # Return the document IDs
            return doc_ids

        except Exception as e:
            logger.error(f"Error during retrieval of document IDs: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during retrieval of document IDs: {e}")

        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection...")
            self.cursor.close()
            self.conn.close()


    def close(self):
        """
        This function closes the cursor and connection.
        :return: None
        """

        # Close the cursor and connection
        logger.info("Closing the cursor and connection...")
        self.cursor.close()
        self.conn.close()
