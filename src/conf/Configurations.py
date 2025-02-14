import logging

from psycopg2.errorcodes import CONFIGURATION_LIMIT_EXCEEDED

# Set up logging configuration (Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()

# Define the chunk size
CHUNK_SIZE = 128

# Define the document type for PDF
DOC_TYPE_FOR_PDF  = "D"

# Define the document type for web data
DOC_TYPE_FOR_WEB = "W"

# Define the number of matches toN be retrieved for semantic retrieval
NUMBER_OF_MATCHES_FOR_SEMANTIC_RETRIEVAL = 3

# Define the number of matches to be retrieved for Tf-Idf
NUMBER_OF_MATCHES_FOR_TF_IDF = 3

# Define the threshold for the LateChunking service
THRESHOLD_FOR_SEMANTIC_RETRIVAL = 0.2

# Define the threshold for the Tf-Idf service
THRESHOLD_FOR_TF_IDF = 0.2

# set the configuration
SEMANTIC_CONFIGURATION = "BOTH"

# Define the URL for the LateChunking service
LATE_CHUNKING_URL = "http://127.0.0.1:8002/retrieve_text/"

# Define the URL for the Tf-Idf service
TF_IDF_URL = "http://127.0.0.1:8002/tf-idf/"

# Define the URL for the retrieval service
RETRIEVAL_URL = "http://127.0.0.1:8002/retrieve/similer_documents/"

# Define the URL for the ollama service
OLLAMA_URL = "http://localhost:8001/llm/ollama/"

# Give the model path for MiniLM-L6-v2
model_path = r"D:\llm\MiniLM-L6-v2"

# Define the database configuration
db_config = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "adisecret",
        "host": "localhost",
        "port": 5432,
    }
