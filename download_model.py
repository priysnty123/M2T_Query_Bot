import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceBgeEmbeddings

# Load environment variables (like EMBEDDING_MODEL_NAME)
load_dotenv()

print("Starting model download...")

# Get the model name from your environment variables
model_name = os.getenv("EMBEDDING_MODEL_NAME")

if model_name:
    try:
        # This line will download the model and cache it
        HuggingFaceBgeEmbeddings(model_name=model_name)
        print(f"Successfully downloaded and cached model: {model_name}")
    except Exception as e:
        print(f"Error downloading model: {e}")
else:
    print("EMBEDDING_MODEL_NAME not found. Skipping download.")