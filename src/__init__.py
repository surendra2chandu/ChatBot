import logging

from psycopg2.errorcodes import CONFIGURATION_LIMIT_EXCEEDED

# Set up logging configuration (Set the logging level to INFO)
logging.basicConfig(level=logging.INFO)

# Get the logger
logger = logging.getLogger()