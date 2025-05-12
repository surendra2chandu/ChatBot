from src import logger
from src.conf.Configurations import db_config
import psycopg2
from psycopg2.extras import execute_values
from fastapi import HTTPException


class ObjDataTable:
    def __init__(self):
        try:
            self.db_config = db_config
            logger.info("Connecting to the database...")
            self.conn = psycopg2.connect(**self.db_config)
            self.cursor = self.conn.cursor()
        except Exception as e:
            logger.error(f"Error during initialization of the database connection: {e}")
            raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

    def store_obj_data_in_db(self, entries):
        """
        Stores heading and text entries in the database.
        :param entries: A list of tuples [(heading1, text1), (heading2, text2), ...]
        """
        try:
            logger.info("Creating table if it does not exist...")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS object_data (
                    doc_id SERIAL PRIMARY KEY,
                    heading TEXT,
                    text TEXT
                );
            """)
        except Exception as e:
            logger.error(f"Error during table creation: {e}")
            raise HTTPException(status_code=500, detail=f"Table creation error: {e}")

        try:

            logger.info("Inserting data into the database...")
            insert_query = """
                INSERT INTO object_data (heading, text)
                VALUES %s
            """
            execute_values(self.cursor, insert_query, entries)
            logger.info(f"Inserting {len(entries)} entries...")
            self.conn.commit()

        except Exception as e:
            logger.error(f"Error during batch insertion: {e}")
            raise HTTPException(status_code=422, detail=f"Batch insertion error: {e}")

        finally:
            logger.info("Closing the cursor and connection...")
            self.cursor.close()
            self.conn.close()
