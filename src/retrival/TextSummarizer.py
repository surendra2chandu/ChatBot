# Import the required modules
from src import logger
from src.utilities import OllamaServiceManager
from src.database_utilities.TfIdf_Table import TfIdfTable


class TextSummarizer:

    @staticmethod
    def summarize(doc_id):
        """
        Summarizes the document text for the given doc_id.
        :param doc_id: The document ID for which to summarize the text.
        :return: The summarized text.
        """

        # Get the document text by ID
        logger.info("Getting the document text by ID.")
        document_text = TfIdfTable().get_document_chunks_by_id(doc_id)
        if not document_text:
            raise "Empty text found for the given doc_id."

        # Summarize the document text using the Ollama service
        logger.info("Summarizing the document text using the Ollama service.")
        summary = OllamaServiceManager.summarize_text(document_text)

        # Return the summary
        return summary



if __name__ == "__main__":
    # Run summarization
    res = TextSummarizer().summarize("doc1")

    print(res)
