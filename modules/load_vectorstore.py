# import os
# from pathlib import Path
# from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# PERSIST_DIR="./chroma_store"
# UPLOAD_DIR="./upload_pdfs"
# os.makedirs(UPLOAD_DIR,exist_ok=True)

# # In your server/modules/load_vectorstore.py file

# import os
# import pypdf
# from typing import List
# from fastapi import UploadFile

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from logger import logger

# # --- Configuration ---
# # It's good practice to define constants at the top
# CHROMA_COLLECTION = "gita_collection"
# EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2"
# BATCH_SIZE = 500 # 👈 Define a batch size that is less than 1000

# # Assuming you have your ChromaDB client setup here as well
# # Make sure this matches the client setup in your main.py
# import chromadb
# CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
# CHROMA_TENANT = os.getenv("CHROMA_TENANT")
# CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")

# client = chromadb.CloudClient(
#      api_key='ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd',
#   tenant='b16c572a-cfe4-4345-aac1-bab73f9eaec2',
#   database='Bhagwat Gita'
# )

# def load_vectorstore(files: List[UploadFile]):
#     """
#     Processes uploaded PDF files, chunks them, and adds them to ChromaDB in batches.
#     """
#     for file in files:
#         # Save the file temporarily to read it
#         temp_filepath = f"./temp_{file.filename}"
#         with open(temp_filepath, "wb") as buffer:
#             buffer.write(file.file.read())

#         # 1. Load the data (you can add your "start from page 10" logic here if needed)
#         reader = pypdf.PdfReader(temp_filepath)
#         text = ""
#         for page in reader.pages:
#             text += page.extract_text()
        
#         os.remove(temp_filepath) # Clean up the temporary file

#         # 2. Chunk the data
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#         chunks = text_splitter.split_documents([text]) # Use split_documents for Document objects
        
#         logger.info(f"Created {len(chunks)} chunks from {file.filename}.")

#         # 3. Create Vector Store object
#         embeddings = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#         vectorstore = Chroma(
#             client=client,
#             collection_name=CHROMA_COLLECTION,
#             embedding_function=embeddings
#         )

#         # 🎯 **THIS IS THE CORRECTED PART** 🎯
#         # Loop through the chunks and add them in batches
#         total_chunks = len(chunks)
#         for i in range(0, total_chunks, BATCH_SIZE):
#             batch = chunks[i:i + BATCH_SIZE]
#             logger.info(f"Uploading batch {i // BATCH_SIZE + 1}/{(total_chunks + BATCH_SIZE - 1) // BATCH_SIZE}...")
#             vectorstore.add_documents(batch) # Use add_documents for Document objects

#     logger.info("All batches have been successfully uploaded.")



# import chromadb
  
# client = chromadb.CloudClient(
#   api_key='ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd',
#   tenant='b16c572a-cfe4-4345-aac1-bab73f9eaec2',
#   database='Bhagwat Gita'
  
# )


# def load_vectorstore(uploaded_files):
#     file_paths=[]
    
#     for file in uploaded_files:
#         save_path = Path(UPLOAD_DIR) / file.filename
#         with open(save_path, "wb") as f:
#             f.write(file.file.read())
#         file_paths.append(str(save_path))
        
#     docs=[]
#     for path in file_paths:
#         loader=PyPDFLoader(path)
#         docs.extend(loader.load())
        
        
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap =200 )
#     texts=splitter.split_documents(docs)
    
#     embeddings=HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")  #sentence-transformers/all-MiniLM-L6-v2  
    
    
#     #new 
#     vectorstore = Chroma(
#         client=client,
#         collection_name="gita_collection", # You can name this whatever you want
#         embedding_function=embeddings,
#     )
    
#     vectorstore.add_documents(texts)
    
#     # if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
#     #     vectorstore=Chroma(persist_directory=PERSIST_DIR,embedding_function=embeddings)
#     #     vectorstore.add_documents(texts)
#     #     vectorstore.persist()
        
#     # else:
#     #     vectorstore=Chroma.from_documents(
#     #         documents=texts,
#     #         embedding=embeddings,
#     #         persist_directory=PERSIST_DIR
#     #     )
#     #     vectorstore.persist()
        
#     return vectorstore



# In: server/modules/load_vectorstore.py

#        CODE FOR MIGRATION

# import os
# import pypdf
# from typing import List
# from fastapi import UploadFile
# from logger import logger
# import chromadb

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # --- 1. Configuration (Loaded from environment variables for security) ---
# CHROMA_API_KEY = os.getenv("CHROMA_API_KEY")
# CHROMA_TENANT = os.getenv("CHROMA_TENANT")
# CHROMA_DATABASE = os.getenv("CHROMA_DATABASE")
# CHROMA_COLLECTION = "gita_collection"
# EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2"
# BATCH_SIZE = 250  # A safe batch size, well below the 1000 limit

# # --- 2. Initialize ChromaDB Client (Once) ---
# # This client object will be reused.
# try:
#     client = chromadb.CloudClient(
#         api_key='ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd',
#         tenant='b16c572a-cfe4-4345-aac1-bab73f9eaec2',
#         database='Bhagwat Gita'
#   )
# except Exception as e:
#     logger.error(f"Failed to initialize ChromaDB client: {e}")
#     # Handle the error appropriately, maybe exit or raise a clearer exception
#     raise

# def load_vectorstore(files: List[UploadFile]):
#     """
#     Processes uploaded PDF files, chunks them, and adds them to ChromaDB in batches.
#     """
#     all_chunks = []
    
#     for file in files:
#         temp_filepath = f"./temp_{file.filename}"
#         with open(temp_filepath, "wb") as buffer:
#             buffer.write(file.file.read())

#         # 1. Load data from PDF
#         try:
#             reader = pypdf.PdfReader(temp_filepath)
#             text = ""
            
            
#             # Or read all pages:
#             for page in reader.pages:
#                 text += page.extract_text()

#         finally:
#             os.remove(temp_filepath)  # Ensure temporary file is always deleted

#         # 2. Chunk the data
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#         # Using `create_documents` to add metadata automatically
#         chunks = text_splitter.create_documents([text], metadatas=[{"source": file.filename}])
#         all_chunks.extend(chunks)
#         logger.info(f"Created {len(chunks)} chunks from {file.filename}.")

#     if not all_chunks:
#         logger.warning("No chunks were created from the uploaded files.")
#         return

#     # 3. Create Vector Store object
#     embeddings = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#     vectorstore = Chroma(
#         client=client,
#         collection_name=CHROMA_COLLECTION,
#         embedding_function=embeddings
#     )

#     # 4. 🎯 Loop through the chunks and add them in batches
#     total_chunks = len(all_chunks)
#     num_batches = (total_chunks + BATCH_SIZE - 1) // BATCH_SIZE
    
#     for i in range(0, total_chunks, BATCH_SIZE):
#         batch = all_chunks[i:i + BATCH_SIZE]
#         batch_num = (i // BATCH_SIZE) + 1
#         logger.info(f"Uploading batch {batch_num}/{num_batches}...")
#         vectorstore.add_documents(documents=batch)

#     logger.info("All batches have been successfully uploaded to ChromaDB.")





# For Durga Durga saptasati


# In server/modules/load_vectorstore.py
# import re
# import os
# import pypdf
# from typing import List
# from fastapi import UploadFile
# from logger import logger
# import chromadb

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # --- Configuration and Client Setup (remains the same) ---
# EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
# BATCH_SIZE = 250
# try:
#     client = chromadb.CloudClient(
#         api_key='ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd',
#         tenant='b16c572a-cfe4-4345-aac1-bab73f9eaec2',
#         database='Bhagwat Gita'
#     )
# except Exception as e:
#     logger.error(f"Failed to initialize ChromaDB client: {e}")
#     raise

# def load_vectorstore(files: List[UploadFile], collection_name: str):
#     all_chunks = []
    
#     for file in files:
#         temp_filepath = f"./temp_{file.filename}"
#         with open(temp_filepath, "wb") as buffer:
#             buffer.write(file.file.read())

#         try:
#             reader = pypdf.PdfReader(temp_filepath)
            
#             # --- START OF CHANGES ---

#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            
#             # 1. Loop through each page to preserve its number
#             for i, page in enumerate(reader.pages):
#                 page_text = page.extract_text()
#                 if not page_text:  # Skip empty pages
#                     continue
                
#                 # 1. Split the page text into individual lines
#                 lines = page_text.split('\n')
#                 english_lines = []
                
#                 # 2. Check each line for Devanagari characters
#                 for line in lines:
#                     # The Devanagari Unicode range is U+0900 to U+097F
#                     # This checks if any character in the line is Hindi/Sanskrit
#                     is_devanagari = any('\u0900' <= char <= '\u097F' for char in line)
                    
#                     # 3. If the line is NOT Devanagari, keep it
#                     if not is_devanagari:
#                         english_lines.append(line)
                
#                 # 4. Join the clean, English-only lines back together
#                 cleaned_text = "\n".join(english_lines)
                
#                 # --- END OF CHANGES ---
                
#                 # Clean the extracted text by removing the tilde character
#                 cleaned_text = page_text.replace('~', '')
                
#                 # --- END OF CHANGE ---

#                 # 2. Create chunks for the CURRENT page's text
#                 page_chunks = text_splitter.create_documents(
                    
#                      # in the durga saptashi i uses [page_text]
                     
#                     [cleaned_text],    # in the durga saptashi i uses [page_text]
                    
                    
#                     # 3. Add metadata with the correct source and page number
#                     metadatas=[{"source": file.filename, "page_number": i + 1}]
#                 )
                
#                 # 4. Add the chunks from this page to our master list
#                 all_chunks.extend(page_chunks)

#             # --- END OF CHANGES ---

#         finally:
#             os.remove(temp_filepath)

#         logger.info(f"Created a total of {len(all_chunks)} chunks from {file.filename}.")

#     if not all_chunks:
#         logger.warning("No chunks were created from the uploaded files.")
#         return

#     # The rest of the function for creating the vectorstore and batch uploading remains the same
#     embeddings = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#     vectorstore = Chroma(
#         client=client,
#         collection_name=collection_name,
#         embedding_function=embeddings
#     )

#     total_chunks = len(all_chunks)
#     for i in range(0, total_chunks, BATCH_SIZE):
#         batch = all_chunks[i:i + BATCH_SIZE]
#         vectorstore.add_documents(documents=batch)

#     logger.info(f"All batches successfully uploaded to collection '{collection_name}'.")


# # In server/modules/load_vectorstore.py


# import re
# import os
# import pypdf
# from typing import List
# from fastapi import UploadFile
# from logger import logger
# import chromadb

# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # --- Configuration and Client Setup (remains the same) ---
# EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
# BATCH_SIZE = 250
# try:
#     client = chromadb.CloudClient(
#         api_key='ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd',
#         tenant='b16c572a-cfe4-4345-aac1-bab73f9eaec2',
#         database='Bhagwat Gita'
#     )
# except Exception as e:
#     logger.error(f"Failed to initialize ChromaDB client: {e}")
#     raise

# def load_vectorstore(files: List[UploadFile], collection_name: str):
#     all_chunks = []
    
#     for file in files:
#         temp_filepath = f"./temp_{file.filename}"
#         with open(temp_filepath, "wb") as buffer:
#             buffer.write(file.file.read())

#         try:
#             reader = pypdf.PdfReader(temp_filepath)
#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            
#             for i, page in enumerate(reader.pages):
#                 page_text = page.extract_text()
#                 if not page_text:
#                     continue
                
               
#                 english_only_text = page_text.encode('ascii', 'ignore').decode()

#                 # Step 2: Now, clean the tildes from the already filtered text
#                 fully_cleaned_text = english_only_text.replace('~', '')

#                 # --- END OF CORRECTED LOGIC ---

#                 # Step 3: Use the fully cleaned text for chunking
#                 page_chunks = text_splitter.create_documents(
#                     [fully_cleaned_text], 
#                     metadatas=[{"source": file.filename, "page_number": i + 1}]
#                 )
                
#                 all_chunks.extend(page_chunks)

#         finally:
#             os.remove(temp_filepath)

#         logger.info(f"Created a total of {len(all_chunks)} chunks from {file.filename}.")

#     if not all_chunks:
#         logger.warning("No chunks were created from the uploaded files.")
#         return

#     # --- The rest of the function remains the same ---
#     embeddings = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)
#     vectorstore = Chroma(
#         client=client,
#         collection_name=collection_name,
#         embedding_function=embeddings
#     )

#     total_chunks = len(all_chunks)
#     for i in range(0, total_chunks, BATCH_SIZE):
#         batch = all_chunks[i:i + BATCH_SIZE]
#         vectorstore.add_documents(documents=batch)

#     logger.info(f"All batches successfully uploaded to collection '{collection_name}'.")


# NEW ONE FOR THE ROUTING FINAL ONE 
import os
import pypdf
from typing import List
from fastapi import UploadFile
from logger import logger
import chromadb
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# --- Global Configuration ---
EMBEDDING_MODEL_NAME = "intfloat/e5-base-v2"
BATCH_SIZE = 250
try:
    # Initialize client and embeddings once to be reused across the application
    client = chromadb.CloudClient(
        api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE")
    )
    embeddings = HuggingFaceBgeEmbeddings(model_name=EMBEDDING_MODEL_NAME)
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB client or embeddings: {e}")
    raise

def get_existing_vectorstore(collection_name: str) -> Chroma:
    """Connects to an existing collection and returns it as a LangChain object."""
    return Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )

def load_vectorstore(files: List[UploadFile], collection_name: str):
    """Processes and uploads a new PDF to a specified collection."""
    all_chunks = []
    for file in files:
        temp_filepath = f"./temp_{file.filename}"
        with open(temp_filepath, "wb") as buffer:
            buffer.write(file.file.read())
        try:
            reader = pypdf.PdfReader(temp_filepath)
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if not page_text: continue
                
                # Cleaning logic to keep only English text
                ascii_text = page_text.encode('ascii', 'ignore').decode()
                fully_cleaned_text = ascii_text.replace('~', '')
                
                page_chunks = text_splitter.create_documents(
                    [fully_cleaned_text], 
                    metadatas=[{"source": file.filename, "page_number": i + 1}]
                )
                all_chunks.extend(page_chunks)
        finally:
            os.remove(temp_filepath)
    
    if not all_chunks: return

    vectorstore = Chroma(
        client=client, collection_name=collection_name, embedding_function=embeddings
    )
    for i in range(0, len(all_chunks), BATCH_SIZE):
        vectorstore.add_documents(documents=all_chunks[i:i + BATCH_SIZE])

    logger.info(f"All batches uploaded to collection '{collection_name}'.")