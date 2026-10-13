"""Build a script that takes a user question, searches the Vector DB,
 and passes the context to an LLM for an answer."""

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

 
 
llm = ChatOpenAI(
    model = "deepseek-chat",
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = 'https://api.deepseek.com',
    max_tokens = 1024,
    temperature = 0.2
)
 
CHROMA_DB = "./Storage_DB"
 
loader = PyPDFLoader("./Resume .pdf") 
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = splitter.split_documents(docs)
embeddings = HuggingFaceEmbeddings(model_name="all-miniLM-L6-v2")  

vectorstore = Chroma.from_documents(
    documents = splits,
    embedding = embeddings,
    persist_directory = CHROMA_DB 
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
 
system_prompt = "You are a helpful assistant. Answer the user question from the retrieved documents."\
"If you dont know an answer, tell that you dont have enough information."\
"Context: {context}"
human_prompt = "{input}"
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", human_prompt),
])
 
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
 
rag_chain = (
    {
        "context": retriever | format_docs,
        "input" : RunnablePassthrough()
    } | prompt_template| llm | StrOutputParser()
)
 
query = "describe about the work experience and the project details"
response = rag_chain.invoke(query)
print(response)
 
 
db_data = vectorstore.get(include=["embeddings", "documents", "metadatas"])
 
first_chunk_text = db_data["documents"][0]
first_chunk_vector = db_data["embeddings"][0]
first_chunk_metadata = db_data["metadatas"][0]
 
print("--- 📄 RAW TEXT CHUNK ---")
print(first_chunk_text)
print(f"\nSource Location: {first_chunk_metadata}")
print("\n--- 🔢 EMBEDDING VECTOR VALUE ---")
print(f"Vector Dimensions: {len(first_chunk_vector)}")
print(f"First 10 numbers of the vector: {first_chunk_vector[:10]}...")
 