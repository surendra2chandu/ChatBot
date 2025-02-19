# Importing the required libraries
from src import logger
from src.conf.Configurations import db_config, NUMBER_OF_MATCHES_FOR_TF_IDF
import psycopg2
from fastapi import HTTPException

class TfIdfTable:
    def __init__(self):
        """                                                        vvvv
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
            logger.error(f"Error connecting to the database: {e}")
            raise HTTPException(status_code=500, detail=f"Error connecting to the database: {e}")

    def store_chunks_in_db(self, file_name, chunks):
        """
        Store the chunks in the database.
        :param file_name: The name of the file.
        :param chunks: The chunks to store.
        :return: None
        """
        try:
            # Create table if not exists
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tf_idf_documents (
                    doc_id TEXT,  -- Unique identifier for each document
                    doc_name TEXT,
                    chunk_id SERIAL PRIMARY KEY,  -- Auto-incrementing chunk ID
                    chunk TEXT NOT NULL
                );
            """)

        except Exception as e:
            logger.error(f"Error creating table: {e}")
            raise HTTPException(status_code=500, detail=f"Error creating table: {e}")

        try:
            # Get the count of unique documents already stored
            # to-do : check other method
            self.cursor.execute("SELECT COUNT(DISTINCT doc_name) FROM tf_idf_documents;")
            doc_count = self.cursor.fetchone()[0]  # Get the count of unique document names

            # Assign a unique doc_id
            doc_id = f"doc{doc_count + 1}"

            for chunk_text in chunks:
                # Insert the data
                self.cursor.execute("INSERT INTO tf_idf_documents (doc_id, doc_name, chunk) VALUES (%s, %s, %s);", (doc_id, file_name, chunk_text))

        except Exception as e:
            logger.error(f"Error inserting data: {e}")
            raise HTTPException(status_code=500, detail=f"Error inserting data: {e}")

        finally:

            logger.info("Committing the transaction.")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def document_exists(self, file_name):
        """
        Checks if a document with the given name already exists in the database.
        :param file_name: Name of the document to check.
        :return: True if document exists, otherwise False.
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM tf_idf_documents WHERE doc_name = %s", (file_name,))
            count = self.cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            if "does not exist" in str(e):  # Adjust based on the actual DB error message
                return False


    def extract_doc_chunks(self):

        try:
            # Fetch relevant columns
            query = """
                SELECT  chunk 
                FROM tf_idf_documents;
            """
            logger.info("Executing query to fetch document chunks...")
            self.cursor.execute(query)
            res = self.cursor.fetchall()

            documents = [row[0] for row in res]

            return documents

        except Exception as e:
            logger.error(f"Error fetching document chunks: {e}")
            return []

        finally:
            self.cursor.close()
            self.conn.close()


    def insert_tf_idf_vector(self, chunks, tf_idf_vector):
        """
        Insert the TF-IDF vector into the database.
        :param chunks: The chunks to insert.
        :param tf_idf_vector: The TF-IDF vector to insert.
        :return: None
        """
        try:
            # Create table if not exists
            self.cursor.execute("""
            ALTER TABLE tf_idf_documents ADD COLUMN IF NOT EXISTS tfidf_vector vector;
            """)

            # Insert the TF-IDF vector
            for doc, vec in zip(chunks,tf_idf_vector):
                self.cursor.execute("""
                    UPDATE tf_idf_documents
                    SET tfidf_vector = %s
                    WHERE chunk = %s;
                """, (vec.tolist(), doc))

        except Exception as e:
            logger.error(f"Error inserting TF-IDF vector: {e}")

        finally:

            # Commit the transaction and close the cursor and connection
            logger.info("Committing the transaction and closing the cursor and connection.")
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def get_similar_documents(self,doc_id,  query_vec):

        try:

            # Query most similar documents using SQL cosine similarity
            logger.info("Querying the most similar documents using SQL cosine similarity.")
            self.cursor.execute("""
                        SELECT chunk, 1 - (tfidf_vector <=> %s::vector) AS similarity
                        FROM tf_idf_documents Where doc_id = %s
                        ORDER BY similarity DESC  -- Lower distance means higher similarity
                        LIMIT %s
                    """, (query_vec.tolist(), doc_id, NUMBER_OF_MATCHES_FOR_TF_IDF))

            # Fetch results
            logger.info("Fetching results.")
            results = self.cursor.fetchall()

            return results

        except Exception as e:
            logger.error(f"Error fetching similar documents: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching similar documents: {e}")

        finally:
            # Close the cursor and connection
            logger.info("Closing the cursor and connection.")
            self.cursor.close()
            self.conn.close()


    def get_document_chunks_by_id(self, doc_id):
        """
        Fetches the document chunks for the given document ID.
        :param doc_id: The document ID.
        :return: The list of document chunks.
        """
        try:
            # Fetch all chunks for the given doc_id
            logger.info(f"Extracting document text for doc_id: {doc_id}")
            self.cursor.execute("""
                        SELECT chunk
                        FROM document_chunks
                        WHERE doc_id = %s
                        ORDER BY chunk_id ASC
                    """, (doc_id,))

            # List of tuples like [(chunk1,), (chunk2,), ...]
            chunks = self.cursor.fetchall()  # List of tuples like [(chunk1,), (chunk2,), ...]

            if not chunks:
                logger.warning(f"No chunks found for doc_id: {doc_id}")
                return ""

            # Convert list of tuples to a single string
            document_text = " ".join(chunk[0] for chunk in chunks)

            return document_text

        except Exception as e:
            logger.error(f"Error fetching document chunks: {e}")
            raise HTTPException(status_code=500, detail=f"Error fetching document chunks: {e}")
