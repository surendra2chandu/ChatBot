# Import required libraries
from src.conf.Configurations import logger, DOC_TYPE_FOR_PDF
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
from src.utilities.LateChunking import LateChunking
from src.utilities.DataBaseUtilities import DataBaseUtility


class InjectionUtility :

    @staticmethod
    def process_text_pipeline(text, file_name):
        """
        Process the text pipeline
        :param text: The text to process
        :param file_name: The name of the file
        :return: None
        """
        # Tokenize and get embeddings
        logger.info("Tokenizing and embedding text...")
        tokens, embeddings = GetTokenEmbeddings().tokenize_and_embed(text)

        # Perform late chunking
        logger.info("Performing late chunking...")
        chunks = LateChunking().late_chunk(tokens, embeddings)

        # Store chunks in database
        logger.info("Storing chunks in the database...")
        DataBaseUtility().store_chunks_in_db(chunks, file_name, DOC_TYPE_FOR_PDF)
