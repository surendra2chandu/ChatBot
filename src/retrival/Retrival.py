# import the necessary libraries
from src import logger
from src.retrival.SemanticRetrival import SemanticRetrival
from src.retrival.Tf_Idf_Retrival import TfIdfRetrival
from fastapi import HTTPException

class Retrival:
    @staticmethod
    def get_similar_documents(query: str, doc_id):
        """
        Get similar documents for the given query using semantic retrival and tf-idf retrival
        :param query: The query for which to find similar documents
        :param doc_id: The document id for which to find similar documents
        :return: The similar documents
        """

        try:
            # Get similar documents using semantic retrival
            logger.info("Retrieving similar documents using semantic retrival")
            semantic_similar_documents = SemanticRetrival().retrieve_relevant_docs(query, doc_id)
            logger.info("similar documents retrieved using semantic retrival")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during semantic retrival: {e}")


        try:
            # Get similar documents using tf-idf retrival
            logger.info("Retrieving similar documents using tf-idf retrival")
            tf_idf_similar_documents = TfIdfRetrival().retrieve_relevant_docs(query, doc_id)
            logger.info("similar documents retrieved using tf-idf retrival")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during tf-idf retrival: {e}")

        # Return the similar documents
        logger.info("Returning the similar documents")
        response = {"semantic_similar_documents": semantic_similar_documents, "tf_idf_similar_documents": tf_idf_similar_documents}

        return response


if __name__ == "__main__":

    sample_query = "this document explores the importance of effective communication in project management it highlights various strategies that enhance team collaboration stakeholder engagement and overall project success modi was born and raised in vadnagar in nor theastern gujarat where he completed his secondary education he was introduced to the rss at the age of eight this document explores the importance of effective communication in project management it highlights various strategies that enhance team collaboration stakeholder engagement and overall project success modi was born and raised in vadnagar in nor theastern gujarat where he completed his secondary education he was introduced to the rss at the age of eight"

   # Get similar documents
    similar_documents = Retrival().get_similar_documents(sample_query, "doc6")

    print(similar_documents)