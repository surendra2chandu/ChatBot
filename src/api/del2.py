from langchain_ollama import OllamaEmbeddings

# Initialize the Ollama embedding model
embedding_model = OllamaEmbeddings(base_url="http://127.0.0.1:11434", model="all-minilm")

# Generate embeddings for a sample text
text = ["The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering The sky is blue because of Rayleigh scattering "]*5000

print(len(text))

# Tokenize the text into words
embedding = embedding_model.embed_documents(text)

print(len(embedding))

print(embedding)  # This will output a list of float numbers
