# import the necessary libraries
from src import logger
from src.retrival.SemanticRetrival import SemanticRetrival
from src.retrival.Tf_Idf_Retrival import TfIdfRetrival
from fastapi import HTTPException

class Retrival:
    @staticmethod
    def get_similer_documents( query: str, doc_id):
        """
        Get similer documents for the given query using semantic retrival and tf-idf retrival
        :param query: The query for which to find similer documents
        :param doc_id: The document id for which to find similer documents
        :return: The similer documents
        """

        try:
            # Get similer documents using semantic retrival
            logger.info("Retrieving similer documents using semantic retrival")
            semantic_similer_documents = SemanticRetrival().retrieve_relevant_docs(query, doc_id)
            logger.info("Similer documents retrieved using semantic retrival")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during semantic retrival: {e}")


        try:
            # Get similer documents using tf-idf retrival
            logger.info("Retrieving similer documents using tf-idf retrival")
            tf_idf_similer_documents = TfIdfRetrival().retrieve_relevant_docs(query, doc_id)
            logger.info("Similer documents retrieved using tf-idf retrival")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred during tf-idf retrival: {e}")

        # Return the similer documents
        logger.info("Returning the similer documents")
        response = {"semantic_similer_documents": semantic_similer_documents, "tf_idf_similer_documents": tf_idf_similer_documents}

        return response


if __name__ == "__main__":

    sample_query = "this document explores the importance of effective communication in project management it highlights various strategies that enhance team collaboration stakeholder engagement and overall project success modi was born and raised in vadnagar in nor theastern gujarat where he completed his secondary education he was introduced to the rss at the age of eight this document explores the importance of effective communication in project management it highlights various strategies that enhance team collaboration stakeholder engagement and overall project success modi was born and raised in vadnagar in nor theastern gujarat where he completed his secondary education he was introduced to the rss at the age of eight"

   # Get similer documents
    similer_documents = Retrival().get_similer_documents(sample_query, "doc6")

    print(similer_documents)