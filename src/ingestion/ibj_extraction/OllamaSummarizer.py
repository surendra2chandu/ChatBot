# Import necessary modules
from src import logger
from fastapi import HTTPException
from langchain_ollama.llms import OllamaLLM


class OllamaSummarizer:
    def __init__(self):
        """
        Initializes the OllamaSummarizer class.
        """

        try:
            # Initialize the Ollama model
            self.model = OllamaLLM(base_url="http://127.0.0.1:11434", model="llama3")
            logger.info("Model initialized.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while initializing the model: {e}")

    def summarize_with_ollama(self, context: str):
        """
        Summarizes the given context using the Ollama model.

        Args:
            context (str): The input text to summarize.

        Returns:
            str: The generated summary.

        Raises:
            HTTPException: If an error occurs during model invocation.
        """

        # System prompt
        system_prompt = """
        Convert the following JSON object into clear, human-understandable language.
    
    Instructions:
    - Do not skip any field unless its value is null.
    - Format date values into a human-readable format (e.g., "2000-07-09T00:00:00" → "July 9, 2000").
    - Do not summarize. Use complete sentences and preserve every piece of data.
    
    Input JSON:
    {
      "DemographicsInfo": {
        "PatientDateOfBirth": "2000-07-09T00:00:00",
        "PatientGender": "M",
        "PatientAddress": "25096 150TH ST",
        "PatientCity": "DIKE",
        "PatientState": "IA",
        "PatientZip": "50624"
      }
    }
    
    Expected Output:
    Demographics Info : The patient's date of birth is July 9, 2000. The gender is male. The permanent address is 25096 150TH Street, located in the city of Dike, in the state of Iowa, with the ZIP code 50624.
    
    """

        # Construct the user prompt
        user_prompt = f"json: {context}"

        # Format the complete prompt for model invocation
        prompt = (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            f"{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
            f"{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"
        )

        try:
            logger.info("Invoking the model with the input prompt.")
            response = self.model.invoke(input=prompt, options={"num_ctx": 4000})
            logger.info("Response received from the model.")

            return response
        except Exception as e:
            logger.error(f"Error during model invocation: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred during invocation: {e}")


if __name__ == "__main__":

    json = """ "LineItems": [
    {
      "id": 258823,
      "ClaimGuid": "10c21da2-1543-4588-b65e-ca2cde711860",
      "ClaimID": 0,
      "InboundFileId": 0,
      "RevenueCode": {
        "Value": "0905",
        "Description": "0905",
        "SequenceOrder": 0
      },
      "Code": "S9480",
      "UnitsBilled": 1.0000,
      "ServiceDateFrom": "2023-07-05T00:00:00",
      "Charges": 455.7100,
      "NonCoveredCharges": 0.0000
    }
  ]"""

    # Generate the summary using the Ollama model
    summary = OllamaSummarizer().summarize_with_ollama(json)
    print(summary)

