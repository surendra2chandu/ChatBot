# import the necessary libraries
from src.retrival.SemanticRetrival import SemanticRetrival
from src.retrival.Tf_Idf_Retrival import TfIdfRetrival
from fastapi import HTTPException
from src.conf.Configurations import logger

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

    sample_query = "50 1 nov 2018 clarification on peomda approval updated lcsp annex requir ements and additional clarification added to aflcmc sample outline 60 30 sep 2019 updated to reflect streamlined lcsp development and coordination process to include product support enterprise review pser and delegation of sustainment command representative scr signature to aflcmclg lz 70 15 oct 2020 updated to reflect streamlined lcsp coordination process for classified programs and policy updates 2 development and coordination of the life cycle sustainment plan lcsp 10 description the lcsp documents the program manager pm and product support managers psm plan for formulating implementing and executing the sustain"
    # Get similer documents for the given query
    similer_documents = Retrival().get_similer_documents(sample_query, "doc_4")

    print(similer_documents)