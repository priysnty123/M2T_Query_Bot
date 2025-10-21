# from fastapi import FastAPI,UploadFile,File,Form,Request
# from fastapi.responses import JSONResponse
# import chromadb
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List
# from modules.load_vectorstore import load_vectorstore
# from modules.llm import get_llm_chain
# from modules.query_handlers import query_chain
# from logger import logger
# import os


# import os
# from dotenv import load_dotenv

# # Load .env from the same directory as this file
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# print("DEBUG: Loaded GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))


# app = FastAPI(Title="RAGBOT")

# # ALLOW FRONTEND
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the RAGBOT API!"}



# @app.middleware("http")
# async def catch_exception_middleware(request:Request,call_next):
#     try:
#         return await call_next(request)
#     except Exception as exc:
#         logger.exception("UNHANDLED EXCEPTION")
#         return JSONResponse(status_code=500,content={"error":str(exc)})
    
    
# @app.post("/upload_pdfs/")
# async def upload_pdfs(files:List[UploadFile]=File(...)):
#     try:
#         logger.info(f"recieved {len(files)} files")
#         load_vectorstore(files)
#         logger.info("documents added to chroma")
#         return {"message":"Files processed and vectorstore updated"}
#     except Exception as e:
#         logger.exception("Error during pdf upload")
#         return JSONResponse(status_code=500,content={"error":str(e)})
    
    
    
# @app.post("/ask/")
# async def ask_quyestion(question:str=Form(...)):
#     try:
#         logger.info("fuser query:{question}")
#         # from langchain.vectorstores import Chroma
#         # from langchain.embeddings import HuggingFaceBgeEmbeddings
#         # from modules.load_vectorstore import PERSIST_DIR

#         # vectorstore=Chroma(
#         #     persist_directory=PERSIST_DIR,
#         #     embedding_function=HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")
#         # )
        
#         client = chromadb.CloudClient(
#             api_key='ck-E7tzkrE7ReVeMbG6dY9iS5jyNuevXoPxCKHjSCJuksMd',
#             tenant='b16c572a-cfe4-4345-aac1-bab73f9eaec2',
#             database='Bhagwat Gita'
  
# )
        
#         vectorstore = Chroma(
#             client=client,
#             collection_name="gita_collection", # This MUST match the name in load_vectorstore
#             embedding_function=HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")
#         )

        
#         chain=get_llm_chain(vectorstore)
#         result=query_chain(chain,question)
#         logger.info("query successfull")
#         return result
#     except Exception as e:
#         logger.exception("error processing question")
#         return JSONResponse(status_code=500,content={"error":str(e)})
    



# @app.get("/test")
# async def test():
#     return {"Message":"Testing sucessful..."}


# @app.get("/about")
# async def about():
#     return {"About": "This project is about the RAG"}


# new for the frontend

# from fastapi import FastAPI, UploadFile, File, Form, Request
# from fastapi.responses import JSONResponse
# import chromadb
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List
# # --- 1. IMPORT THE 'client' OBJECT FROM YOUR MODULE ---
# from modules.load_vectorstore import load_vectorstore, client 
# from modules.llm import get_llm_chain
# from modules.query_handlers import query_chain
# from logger import logger
# import os
# from dotenv import load_dotenv

# # Load .env
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# app = FastAPI(Title="RAGBOT")

# # CORS Middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the RAGBOT API!"}

# @app.middleware("http")
# async def catch_exception_middleware(request:Request, call_next):
#     try:
#         return await call_next(request)
#     except Exception as exc:
#         logger.exception("UNHANDLED EXCEPTION")
#         return JSONResponse(status_code=500, content={"error": str(exc)})
    
    
# @app.post("/upload_pdfs/")
# # --- 2. MODIFIED TO ACCEPT 'collection_name' ---
# async def upload_pdfs(
#     collection_name: str = Form(...), 
#     files: List[UploadFile] = File(...)
# ):
#     try:
#         logger.info(f"Received {len(files)} files for collection: '{collection_name}'")
#         # Pass the collection_name to your function
#         load_vectorstore(files, collection_name) 
#         logger.info(f"Documents added to chroma collection '{collection_name}'")
#         return {"message": f"Files processed and added to collection '{collection_name}'"}
#     except Exception as e:
#         logger.exception("Error during pdf upload")
#         return JSONResponse(status_code=500, content={"error": str(e)})
    
    
# @app.post("/ask/")
# # --- 3. MODIFIED TO ACCEPT 'collection_name' ---
# async def ask_question(
#     question: str = Form(...), 
#     collection_name: str = Form(...)
# ):
#     try:
#         logger.info(f"User query for collection '{collection_name}': {question}")

#         # --- 4. CLEANUP ---
#         # No need to create a new client here, we imported the global one.
#         # Use the provided collection_name to connect to the correct collection.
#         vectorstore = Chroma(
#             client=client,
#             collection_name=collection_name, 
#             embedding_function=HuggingFaceBgeEmbeddings(model_name="intfloat/e5-base-v2")
#         )

#         chain = get_llm_chain(vectorstore)
#         result = query_chain(chain, question)
#         logger.info("Query successful")
#         return result
#     except Exception as e:
#         logger.exception("error processing question")
#         return JSONResponse(status_code=500, content={"error": str(e)})
    
    
# # --- 5. NEW ENDPOINT ADDED ---
# @app.get("/collections/")
# async def get_collections():
#     """
#     Returns a list of all collection names in the database.
#     """
#     try:
#         # We use the imported 'client' object
#         collections = client.list_collections() 
#         collection_names = [c.name for c in collections]
#         logger.info(f"Found collections: {collection_names}")
#         return {"collections": collection_names}
#     except Exception as e:
#         logger.exception("Could not retrieve collections.")
#         return JSONResponse(status_code=500, content={"error": str(e)})


# @app.get("/test")
# async def test():
#     return {"Message": "Testing successful..."}


# @app.get("/about")
# async def about():
#     return {"About": "This project is about the RAG"}


# New onw routing wala 
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import load_vectorstore, get_existing_vectorstore, client
from modules.llm import get_multi_retriever_chain
from logger import logger
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = FastAPI(Title="RAGBOT")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Welcome to the RAGBOT API!"}

# This is CRITICAL. The LLM router uses these descriptions
# to decide which collection to use. Make sure the names match your collections.
COLLECTION_METADATA = {
    "gita_collection": "Good for questions about philosophy, life, duty, 'Soul Quest', and Krishna. Based on the Bhagavad Gita.",
    "ramayana_full": "Good for questions about stories, 'Soul Quest', duty, and relationships, based on the epic Ramayana.",
    "Durga_Saptasati": "Good for questions about the divine feminine, goddesses, mantras, and stories related to Goddess Durga.",
    "Yajurveda": "Good for questions about specific ancient rituals, yajnas, and hymns."
}

@app.middleware("http")
async def catch_exception_middleware(request:Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500, content={"error": str(exc)})
    
@app.post("/upload_pdfs/")
async def upload_pdfs(collection_name: str = Form(...), files: List[UploadFile] = File(...)):
    try:
        load_vectorstore(files, collection_name) 
        return {"message": f"Files processed and added to collection '{collection_name}'"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.post("/ask/")
# The endpoint no longer needs 'collection_name' from the user
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"Router query received: {question}")
        retriever_infos = []
        available_collections = [c.name for c in client.list_collections()]
        
        for name in available_collections:
            if name in COLLECTION_METADATA:
                vectorstore = get_existing_vectorstore(name)
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                retriever_infos.append({
                    "name": name,
                    "description": COLLECTION_METADATA[name],
                    "retriever": retriever
                })

        if not retriever_infos:
            return JSONResponse(status_code=500, content={"error": "No retrievers configured."})

        # Create and run the router chain
        chain = get_multi_retriever_chain(retriever_infos)
        result = chain.invoke({"input": question}) 

        # Correctly format the response to return a list of dictionaries
        source_metadata = [doc.metadata for doc in result.get("source_documents", [])]
        response = {"response": result["result"], "sources": source_metadata}
        
        logger.info("Router query successful")
        return response
        
    except Exception as e:
        logger.exception("Error processing router question")
        return JSONResponse(status_code=500, content={"error": str(e)})
    
@app.get("/collections/")
async def get_collections():
    try:
        collections = client.list_collections() 
        return {"collections": [c.name for c in collections]}
    except Exception as e:
        logger.exception("Could not retrieve collections.")
        return JSONResponse(status_code=500, content={"error": str(e)})