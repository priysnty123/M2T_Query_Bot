# # migrate.py

# import chromadb
# from logger import logger # Assuming your logger is accessible
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# def migrate_collections():
#     """
#     Fetches documents from a source ChromaDB collection and adds them 
#     to a destination collection, re-embedding them in the process.
#     """
#     try:
#         # --- 1. Connect to the SOURCE database (Ramayana) ---
#         logger.info("Connecting to SOURCE ChromaDB cloud...")
#         source_client = chromadb.CloudClient(
#                 api_key="ck-HfcokCUyqmwyhEbLucxY7RevVhS8VERwvomt7ao83CLH",
#                 tenant="04bfb534-7412-4bf4-a84c-a136baf54831",       
#                 database="Ramayana"
#         )
#         source_collection = source_client.get_collection("Ramayana_batch1")
#         logger.info(f"Successfully connected to source collection 'Ramayana_batch1'.")

#         # --- 2. Fetch all data from the SOURCE collection ---
#         logger.info("Fetching all documents and metadata from source...")
#         # The .get() method without IDs fetches everything.
#         source_data = source_collection.get(include=["documents", "metadatas"])
        
#         # We need the documents, metadatas, and a unique ID for each item.
#         documents_to_add = source_data['documents']
#         metadatas_to_add = source_data['metadatas']
#         # We must create new unique IDs for the destination.
#         ids_to_add = [f"ramayana_doc_{i}" for i in range(len(documents_to_add))]

#         logger.info(f"Fetched {len(documents_to_add)} documents to migrate.")

#         # --- 3. Connect to your DESTINATION database (Bhagwat Gita) ---
#         logger.info("Connecting to DESTINATION ChromaDB cloud...")
#         destination_client = chromadb.CloudClient(
#             api_key="ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd", # Your API key
#             tenant="b16c572a-cfe4-4345-aac1-bab73f9eaec2",          # Your tenant
#             database='Bhagwat Gita'                         # Your database
#         )
        
#         # --- 2. DEFINE YOUR EMBEDDING MODEL ---
#         embedding_function = HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")

#         # --- 3. PASS THE MODEL WHEN GETTING THE COLLECTION ---
#         destination_collection = destination_client.get_or_create_collection(
#             name="gita_collection",
#             embedding_function=embedding_function.embed_documents # Use the LangChain wrapper's function
#         ) 
            
            
#         destination_collection = destination_client.get_or_create_collection("gita_collection")
#         logger.info(f"Successfully connected to destination collection 'gita_collection'.")

#         # --- 4. Add the fetched data to your DESTINATION collection ---
#         # ChromaDB will automatically handle embedding the documents with your model.
#         logger.info("Adding documents to the destination collection. This may take a while...")
#         destination_collection.add(
#             ids=ids_to_add,
#             documents=documents_to_add,
#             metadatas=metadatas_to_add
#         )
        
#         logger.info("✅ Migration complete! All documents have been added and re-embedded.")

#     except Exception as e:
#         logger.error(f"An error occurred during migration: {e}")
#         logger.exception("Migration script failed.")

# if __name__ == "__main__":
#     migrate_collections()



# migrate.py

# import chromadb
# from logger import logger
# # --- 1. IMPORT THE REQUIRED LANGCHAIN COMPONENTS ---
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from langchain_core.documents import Document

# def migrate_collections():
#     """
#     Fetches documents from a source ChromaDB collection and adds them
#     to a destination collection, re-embedding them in the process.
#     """
#     try:
#         # --- (Source connection code remains the same) ---
#         logger.info("Connecting to SOURCE ChromaDB cloud...")
#         source_client = chromadb.CloudClient(
#                 api_key="ck-HfcokCUyqmwyhEbLucxY7RevVhS8VERwvomt7ao83CLH",
#                 tenant="04bfb534-7412-4bf4-a84c-a136baf54831",       
#                 database="Ramayana"
#         )
#         source_collection = source_client.get_collection("Ramayana_batch1")
#         logger.info("Successfully connected to source collection 'Ramayana_batch1'.")

#         logger.info("Fetching all documents and metadata from source...")
#         source_data = source_collection.get(include=["documents", "metadatas"],
#                         limit=2000          
        
#         )
        
#         documents_to_add = source_data['documents']
#         metadatas_to_add = source_data['metadatas']
#         # We must create new unique IDs for the destination.
#         ids_to_add = [f"ramayana_doc_{i}" for i in range(len(documents_to_add))]
#         logger.info(f"Fetched {len(documents_to_add)} documents to migrate.")

#         # --- 2. CONNECT TO YOUR DESTINATION DATABASE ---
#         logger.info("Connecting to DESTINATION ChromaDB cloud...")
#         destination_client = chromadb.CloudClient(
#             api_key="ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd", # Your API key
#             tenant="b16c572a-cfe4-4345-aac1-bab73f9eaec2",          # Your tenant
#             database='Bhagwat Gita'                         # Your database
#         )
        
#         # --- 3. CREATE THE LANGCHAIN VECTOR STORE FOR THE DESTINATION ---
#         # This object will correctly manage the client and the embedding function.
#         embedding_function = HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")
#         destination_vectorstore = Chroma(
#             client=destination_client,
#             collection_name="Ramayana",
#             embedding_function=embedding_function,
#         )
#         logger.info(f"Successfully connected to destination collection 'gita_collection'.")

#         # --- 4. FORMAT DATA INTO LANGCHAIN DOCUMENT OBJECTS ---
#         # The .add_documents method expects this specific format.
#         docs_to_add_as_langchain_docs = []
#         for i, doc_text in enumerate(documents_to_add):
#             metadata = metadatas_to_add[i] if metadatas_to_add and i < len(metadatas_to_add) else {}
#             docs_to_add_as_langchain_docs.append(
#                 Document(page_content=doc_text, metadata=metadata)
#             )

#         # --- 5. USE THE LANGCHAIN METHOD TO ADD DOCUMENTS ---
#         # This will correctly handle the embedding and adding process.
#         logger.info("Adding documents to the destination collection. This may take a while...")
#         destination_vectorstore.add_documents(
#             documents=docs_to_add_as_langchain_docs, 
#             ids=ids_to_add
#         )
        
#         logger.info("✅ Migration complete! All documents have been added and re-embedded.")

#     except Exception as e:
#         logger.error(f"An error occurred during migration: {e}")
#         logger.exception("Migration script failed.")

# if __name__ == "__main__":
#     migrate_collections()



# migrate.py

# migrate.py

import chromadb
from logger import logger
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.documents import Document

def migrate_collections():
    try:
        # --- (Fetching logic is correct and remains the same) ---
        logger.info("Connecting to SOURCE ChromaDB cloud...")
        source_client = chromadb.CloudClient(
            api_key="ck-HfcokCUyqmwyhEbLucxY7RevVhS8VERwvomt7ao83CLH",
            tenant="04bfb534-7412-4bf4-a84c-a136baf54831",
            database="Ramayana"
        )
        source_collection_name = "Ramayana_batch1"
        source_collection = source_client.get_collection(source_collection_name)
        logger.info(f"Successfully connected to source collection '{source_collection_name}'.")

        logger.info("Fetching all documents in batches to respect source quota...")
        all_documents = []
        all_metadatas = []
        offset = 0
        fetch_limit = 300

        while True:
            source_data = source_collection.get(
                include=["documents", "metadatas"],
                limit=fetch_limit,
                offset=offset
            )
            batch_docs = source_data['documents']
            if not batch_docs: break
            
            all_documents.extend(batch_docs)
            all_metadatas.extend(source_data['metadatas'])
            offset += len(batch_docs)
            logger.info(f"Fetched batch. Total documents retrieved so far: {offset}")

        logger.info(f"Finished fetching. Total documents to migrate: {len(all_documents)}.")

        # --- (Destination connection and setup remains the same) ---
        logger.info("Connecting to DESTINATION ChromaDB cloud...")
        destination_client = chromadb.CloudClient(
            api_key="ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd",
            tenant="b16c572a-cfe4-4345-aac1-bab73f9eaec2",
            database='Bhagwat Gita'
        )
        embedding_function = HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")
        destination_vectorstore = Chroma(
            client=destination_client,
            collection_name="ramayana_full",
            embedding_function=embedding_function,
        )
        logger.info(f"Successfully connected to destination collection 'ramayana_full'.")

        # --- (Formatting into LangChain documents remains the same) ---
        docs_to_add_as_langchain_docs = []
        for i, doc_text in enumerate(all_documents):
            metadata = all_metadatas[i] if all_metadatas and i < len(all_metadatas) else {}
            docs_to_add_as_langchain_docs.append(
                Document(page_content=doc_text, metadata=metadata)
            )
        ids_to_add = [f"ramayana_doc_{i}" for i in range(len(docs_to_add_as_langchain_docs))]

        # --- NEW BATCHING LOGIC FOR ADDING DOCUMENTS ---
        logger.info("Adding documents to the new collection in batches...")
        add_batch_size = 300 # Respects the destination's limit
        
        for i in range(0, len(docs_to_add_as_langchain_docs), add_batch_size):
            batch_docs = docs_to_add_as_langchain_docs[i:i + add_batch_size]
            batch_ids = ids_to_add[i:i + add_batch_size]
            
            destination_vectorstore.add_documents(
                documents=batch_docs, 
                ids=batch_ids
            )
            logger.info(f"Added batch {i//add_batch_size + 1} with {len(batch_docs)} documents.")
        # --- END OF NEW LOGIC ---
        
        logger.info(f"✅ Migration complete! Total documents migrated: {len(docs_to_add_as_langchain_docs)}.")

    except Exception as e:
        logger.error(f"An error occurred during migration: {e}")
        logger.exception("Migration script failed.")

if __name__ == "__main__":
    migrate_collections()