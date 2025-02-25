# Import necessary libraries , classes and functions
from src import logger
from src.ingestion.Tf_Idf_Injector import TfIdfInjector
from src.database_utilities.TfIdf_Table import TfIdfTable
from fastapi import HTTPException


class TfIdfRetrival:

    @staticmethod
    def retrieve_relevant_docs(query: str, doc_id: str):
        """
        Extracts documents similar to the query using TF-IDF.
        :param query: The query to search for.
        :param doc_id: The document id to search for.
        :return: The list of tuples containing the document text and similarity score.
        """
        try:
            # Initialize the TF-IDF injector
            logger.info("Initializing the TF-IDF injector.")
            vectorizer = TfIdfInjector().get_vectorizer()

            # Transform query to TF-IDF vector
            logger.info("Transforming the query to a TF-IDF vector.")
            query_vec = vectorizer.transform([query]).toarray()[0]
        except Exception as e:
            logger.info(f"Error in transforming the query to a TF-IDF vector: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during transformation: {e}")

        # Query most similar documents using SQL cosine similarity
        logger.info("Querying the most similar documents using SQL cosine similarity.")
        results = TfIdfTable().get_similar_documents(doc_id, query_vec)

        return results


# Run retrieval
if __name__ == "__main__":
    sample_query="air force life cycle management center standard process for life cycle sustainment plans lcsp process owner aflcmclg lz date 15 october 2020 version 7 0 1 record of changes record of changes version effective date summary 10 1 apr 2016 basic document approved by standard process sp board on 24 mar 16 20 1 jul 2016 updated to reflect afmccc delegation of sustainment command representative requirement for acat ii and below programs to center commanders 30 30 jul 2017 updated to reflect osd sample outline version 20 and other aflcmc level process improvements 40 1 oct 2017 administrative update to reflect updated afi 6310120 101 dtd 9 may 2017 reference changes"
    top_docs = TfIdfRetrival().retrieve_relevant_docs(sample_query, "doc1")

    for doc, score in top_docs:
        print(f"Document: {doc} | Similarity Score: {score:.4f}")
