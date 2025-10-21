
import os
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

print("--- SERVER IS LOADING THE CORRECT AND NEWEST LLM.PY FILE ---")

def get_multi_retriever_chain(retriever_infos: list):
    """
    Implements manual routing across multiple retrievers.
    Avoids the broken MultiRetrievalQAChain API.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found.")

    llm = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile")
    
    prompt_template = """
You are an expert assistant specialized in ancient Indian scriptures and wisdom texts.
Use the provided context to answer the user's question accurately and compassionately.

If the context doesn't contain relevant information, clearly state that.

Context: {context}
Question: {question}

Helpful Answer:
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )

    # Create RetrievalQA chains for each retriever
    chains = {}
    for info in retriever_infos:
        name = info["name"]
        retriever = info["retriever"]
        
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        chains[name] = chain
    
    # Create a router chain that decides which retriever to use
    router_prompt = PromptTemplate(
        template="""Given the following question and collection descriptions, 
decide which collection is best suited to answer it. Respond with ONLY the collection name, nothing else.

Collections:
{descriptions}

Question: {question}

Collection name:""",
        input_variables=["descriptions", "question"]
    )
    
    descriptions = "\n".join([
        f"- {info['name']}: {info['description']}"
        for info in retriever_infos
    ])
    
    # Return a wrapper object that handles routing
    class RoutingChain:
        def __init__(self, chains, llm, router_prompt, descriptions):
            self.chains = chains
            self.llm = llm
            self.router_prompt = router_prompt
            self.descriptions = descriptions
        
        def invoke(self, input_dict):
            question = input_dict.get("input", "")
            
            # Route the question
            routing_input = self.router_prompt.format(
                descriptions=self.descriptions,
                question=question
            )
            route_decision = self.llm.invoke(routing_input).content.strip()
            
            # Sanitize the route decision (remove extra text)
            selected_chain_name = None
            for chain_name in self.chains.keys():
                if chain_name.lower() in route_decision.lower():
                    selected_chain_name = chain_name
                    break
            
            if not selected_chain_name:
                selected_chain_name = list(self.chains.keys())[0]
            
            print(f"Router selected: {selected_chain_name} for question: {question}")
            
            # Use the selected chain
            chain = self.chains[selected_chain_name]
            result = chain.invoke({"query": question})
            
            return {
                "result": result.get("result", ""),
                #"source_documents": result.get("source_documents", []),
                "selected_collection": selected_chain_name
            }
    
    return RoutingChain(chains, llm, router_prompt, descriptions)


































# ye routing k liye best hai 

# import os
# from langchain_groq import ChatGroq
# from langchain.chains import MultiRetrievalQAChain
# from langchain.prompts import PromptTemplate

# print("--- SERVER IS LOADING THE CORRECT AND NEWEST LLM.PY FILE ---")

# def get_multi_retriever_chain(retriever_infos: list):
#     """
#     Creates a chain that routes queries to the appropriate retriever
#     and then answers the question.
#     """
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         raise ValueError("GROQ_API_KEY not found.")

#     llm = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile")
    
#     prompt_template = """
# You are an expert assistant specialized in ancient Indian scriptures and wisdom texts.
# Use the provided context to answer the user's question accurately and compassionately.

# If the context doesn't contain relevant information, clearly state that.

# Context: {context}
# Question: {question}

# Helpful Answer:
#     """
    
#     PROMPT = PromptTemplate(
#         template=prompt_template, 
#         input_variables=["context", "question"]
#     )

#     # MultiRetrievalQAChain will create its own internal chains
#     # Just pass the LLM, retriever_infos, and prompt customization
#     chain = MultiRetrievalQAChain.from_retrievers(
#         llm=llm,
#         conversation_llm=llm,
#         retriever_infos=retriever_infos,
#         chain_type_kwargs={"prompt": PROMPT},
#         return_source_documents=True,
#         verbose=True
#     )
    
#     return chain














# import os
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate # STEP 1: Import the class

# def get_llm_chain(vectorstore):
#     api_key = os.getenv("GROQ_API_KEY")

#     if not api_key:
#         raise ValueError("❌ GROQ_API_KEY not found. Make sure .env is loaded and key is set correctly.")
    

#     prompt_template = """
# # ROLE AND GOAL
# You are "Jnana-Bot," an expert and compassionate guide to the Bhagavad Gita. Your purpose is to provide solace and clear answers based on the teachings of Lord Krishna, using the provided text.

# # CRITICAL RULE: USE PROVIDED TEXT ONLY
# **Your answers MUST be 100%  derived from the `Context` provided below.** Do not use any of your own internal knowledge, training data, or external information. If the answer is not in the `Context`, you MUST state that the provided text does not contain the answer. Your knowledge is strictly confined to the text I provide you.

# # SCRIPTURAL REFERENCE GUIDE
# This guide maps user concerns to key verses. You must use this as your primary source of truth for generating answers.

# **Anger:** (Feelings of rage, frustration, or resentment) - Chapter 2 (Text 56, 62, 63), Chapter 5 (Text 26), Chapter 16 (Text 1-3, 21).
# **Fear:** (Anxiety, worry, or being afraid of outcomes) - Chapter 4 (Text 10), Chapter 11 (Text 50), Chapter 18 (Text 30).
# **Lust:** (Overwhelming desire or material craving) - Chapter 3 (Text 37, 41, 43), Chapter 5 (Text 22), Chapter 16 (Text 21).
# **Confusion:** (Feeling lost, uncertain, or unable to make a decision.) - Chapter 2 (Text 7), Chapter 3 (Text 2), Chapter 18 (Text 61).
# **Feeling Sinful:** (Guilt, shame, or feeling morally wrong.) - Chapter 4 (Text 36), Chapter 5 (Text 10), Chapter 9 (Text 30), Chapter 14 (Text 6), Chapter 18 (Text 66).
# **Practicing Forgiveness:** (The struggle to let go of grudges.) - Chapter 11 (Text 44), Chapter 12 (Text 13-14), Chapter 16 (Text 1-3).
# **Dealing With Envy:** (Jealousy towards others' success or possessions.) - Chapter 12 (Text 13-14), Chapter 16 (Text 19), Chapter 18 (Text 71).
# **Forgetfulness:** (Forgetting one's spiritual purpose or duties.) - Chapter 15 (Text 15), Chapter 18 (Text 61).
# **Pride:** (Arrogance, ego, or a feeling of superiority.) - Chapter 16 (Text 4, 13-15), Chapter 18 (Text 26, 58).
# **Death of a Loved One:** (Grief and sorrow from loss.) - Chapter 2 (Text 13, 20, 22, 25, 27).
# **Greed:** (An intense desire for more wealth or material things.) - Chapter 14 (Text 17), Chapter 16 (Text 21), Chapter 17 (Text 25).
# **Seeking Peace:** (A desire for inner calm and tranquility.) - Chapter 2 (Text 66, 71), Chapter 4 (Text 39), Chapter 5 (Text 29), Chapter 8 (Text 28).
# **Demotivated:** (Lacking motivation, purpose, or drive.) - Chapter 11 (Text 33), Chapter 18 (Text 48, 78).
# **Laziness:** (Aversion to effort or spiritual practice.) - Chapter 3 (Text 8), Chapter 5 (Text 20), Chapter 6 (Text 16), Chapter 18 (Text 39).
# **Temptation:** (Being drawn towards worldly or negative actions.) - Chapter 2 (Text 60, 61, 70), Chapter 7 (Text 14).
# **Depression:** (Feelings of deep sadness, despair, or hopelessness.) - Chapter 2 (Text 3, 14), Chapter 5 (Text 21).
# **Loneliness:** (Feeling isolated, alone, or disconnected.) - Chapter 6 (Text 30), Chapter 9 (Text 29), Chapter 13 (Text 16, 18).
# **Uncontrolled Mind:** (A restless, agitated, or wandering mind.) - Chapter 6 (Text 5, 6, 26, 35).
# **Discriminated / Losing Hope:** (Feeling unjustly treated or that all is lost.) - Chapter 5 (Text 18, 19), Chapter 6 (Text 32), Chapter 9 (Text 29), Chapter 18 (Text 34, 66, 78).

# # TASK EXECUTION:
# When you receive a user's question, you MUST follow this precise three-step process:

# **Step 1: Analyze and Categorize the User's Query.**
# Silently analyze the user's question to understand the underlying emotional or spiritual problem. Categorize the query into **ONE** of the categories listed in the **Scriptural Reference Guide**.

# **Step 2: Locate the Guiding Verses.**
# After identifying the category, refer back to the **Scriptural Reference Guide** to find the specific Chapter and Text numbers associated with it. Your primary task is now to locate the teachings from these exact verses within the provided `Context`.

# **Step 3: Synthesize a Focused Answer.**
# Construct your answer giving **highest priority** to the wisdom found in the guided verses you located in Step 2. Your response must be a direct and comforting solution to the user's problem, based entirely on these specific scriptural references from the `Context`.

# ---
# Context: {context}
# ---
# Question: {question}
# ---

# # REQUIRED OUTPUT STRUCTURE
# **1. Direct Answer:** Begin with a concise, one or two-sentence summary that directly answers the question based on the specific verses from the context.
# **2. Detailed Explanation:** Elaborate on the answer. Explain the relevant teachings from the specific verses that address the user's categorized problem.
# **3. Scriptural Evidence:** Conclude with a direct quotation or a summary of a key passage from the specific verses in the `Context` that supports your answer.

# Helpful Answer:

# """
    
#     # STEP 2: Use the PromptTemplate CLASS to create the object
#     PROMPT = PromptTemplate(
#         template=prompt_template, input_variables=["context", "question"]
#     )

#     llm = ChatGroq(
#         api_key=api_key,
#         model="llama-3.3-70b-versatile" 
#     )

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": PROMPT} # Pass the correctly created prompt object
#     )





















# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA

# load_dotenv()

# # GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# def get_llm_chain(vectorstore):
#     api_key = os.getenv("GROQ_API_KEY")
#     llm = ChatGroq(
#         api_key=api_key,
#         model="llama3-70b-8192"
#     )

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True
#     )


# import os

# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA

# # load_dotenv()

# def get_llm_chain(vectorstore):
#     api_key = os.getenv("GROQ_API_KEY")

#     if not api_key:
#         raise ValueError("❌ GROQ_API_KEY not found. Make sure .env is loaded and key is set correctly.")
    
    
#     prompt_template = """
    
# Introduction: 
# You are "Query-Bot" ,an expert AI assistant specializing in the wisdom of ancient Indian scriptures. Your sole purpose is to provide accurate, context-aware, and faithful answers based EXCLUSIVELY on the provided context. You are a scholarly guide, not a spiritual guru.

# STRICT CONSTRAINTS & GUIDING PRINCIPLES
#     1.  **Absolute Textual Fidelity:** Your answers MUST be 100%  grounded in the provided `Context`. Do not infer, speculate, or introduce any external information, modern commentary, or personal opinions. Your knowledge is confined strictly to the text provided below.
#     2.  **The "I Don't Know" Protocol:** If the `Context` does not contain a specific or clear answer to the `Question`, you MUST state: "The provided scriptures do not contain a direct answer to this specific question." Do not attempt to create an answer.
#     3.  **Neutral, Scholarly Tone:** Your tone should be respectful, impartial, and academic.
#     4.  **Clarity and Precision:** Use pure, clear English. Define any Sanskrit terms you use (e.g., "Dharma (duty/righteousness)").

# TASK EXECUTION:
#     1.Use the following pieces of `Context`, which are retrieved passages from the scriptures, to answer the user's `Question`. You must follow the "Required Output Structure" for the response.

# ---
# Context: {context}
# ---
# Question: {question}
# ---

# REQUIRED OUTPUT STRUCTURE:
#     1. Direct Answer: Begin with a concise, one or two-sentence summary that directly answers the question based on the context.
#     2. Detailed Explanation: Elaborate on the direct answer. Provide the necessary narrative background, characters involved, and the sequence of events as described in the provided `Context`.
#     3. Scriptural Evidence: Conclude with a direct quotation or a summary of a key passage from the `Context` that supports your answer. Provide a precise citation if it is available within the source metadata.


# Helpful Answer:
    
#     """
    
#     Prompt = prompt_template(
#         template=prompt_template, input_variables=["context", "question"]
#     )

#     llm = ChatGroq(
#         api_key=api_key,
#         model="llama-3.3-70b-versatile"
#     )

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": Prompt}
#     )
    
 

# import os
# from langchain_groq import ChatGroq
# from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate # 👈 STEP 1: Import PromptTemplate

# def get_llm_chain(vectorstore):
#     api_key = os.getenv("GROQ_API_KEY")

#     if not api_key:
#         raise ValueError("❌ GROQ_API_KEY not found. Make sure .env is loaded and key is set correctly.")

#     # 👇 STEP 2: Define your custom prompt template
#     prompt_template = """
#     You are a helpful assistant for answering questions based on the provided documents.
#     Use the following pieces of context to answer the user's question.
#     If you don't know the answer from the context provided, just say that you don't know, don't try to make up an answer.
#     Be concise and helpful.

#     Context: {context}
#     Question: {question}
    
#     Helpful Answer:
#     """

#     PROMPT = PromptTemplate(
#         template=prompt_template, input_variables=["context", "question"]
#     )

#     llm = ChatGroq(
#         api_key=api_key,
#         model="llama3-70b-8192"
#     )

#     retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

#     # 👇 STEP 3: Modify the RetrievalQA chain to use your new prompt
#     return RetrievalQA.from_chain_type(
#         llm=llm,
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True,
#         chain_type_kwargs={"prompt": PROMPT} # Pass the prompt here
#     )