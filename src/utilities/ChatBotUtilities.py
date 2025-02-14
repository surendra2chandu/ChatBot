from src.conf.Configurations import THRESHOLD_FOR_SEMANTIC_RETRIVAL, THRESHOLD_FOR_TF_IDF, logger

def get_sematic_similer_documents_text(similer_documents):
    """
    Function to get the text from the semantically similer documents
    :param similer_documents: The similer documents
    :return: The text from the similer documents
    """

    # Initialize the context
    context = ""

    # Get the text from the semantically similer documents
    logger.info("Getting the text from the semantically similer documents...")
    for doc in similer_documents["semantic_similer_documents"]:
        if doc[1] >= THRESHOLD_FOR_SEMANTIC_RETRIVAL:
            context += doc[0] + " "

    # Return the context
    return context

def get_tf_idf_similer_documents_text(similer_documents):
    """
    Function to get the text from the Tf-Idf similer documents
    :param similer_documents: The similer documents
    :return: The text from the similer documents
    """

    # Initialize the context
    context = ""

    # Get the text from the Tf-Idf similer documents
    logger.info("Getting the text from the Tf-Idf similer documents...")
    for doc in similer_documents["tf_idf_similer_documents"]:
        if doc[1] >= THRESHOLD_FOR_TF_IDF:
            context += doc[0] + " "

    # Return the context
    return context