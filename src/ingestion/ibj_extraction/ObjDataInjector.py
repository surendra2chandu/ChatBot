from src.ingestion import ibj_extraction
import json
from src.ingestion.ibj_extraction.OllamaSummarizer import OllamaSummarizer
from src.database_utilities.ObjDataTable import ObjDataTable
from src import logger

class ObjDataInjector:
    def __init__(self):
        """
        Initializes the ObjDataInjector class.
        """
        pass

    def inject_data(self):
        """
        Injects data into the database.
        """

        # Load the JSON data from the file
        logger.info("Loading JSON data from file...")
        with open('data.json', 'r') as file:
            d = json.load(file)

        data = []

        # Convert each item in the dictionary to a JSON string with key-value pairs
        for key, value in d.items():
            json_string = f'"{key}" : {json.dumps(value)}'

            # Generate the summary using the Ollama model
            text = OllamaSummarizer().summarize_with_ollama(json_string)

            # Append the heading and text to the data list
            data.append((key, text))

        # data = [("heading1", "text1"), ("heading2", "text2"), ("heading3", "text3")]

        # Store the data in the database
        ObjDataTable().store_obj_data_in_db(data)


if __name__ == "__main__":
    injector = ObjDataInjector()
    injector.inject_data()
