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

loader = PyPDFLoader("./course.pdf") #docx2txtloader, #textloader, #csvloader, #UnstructuredURLloader(or)    webbaseloader, #directoryloader
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = splitter.split_documents(docs)
 
embeddings = HuggingFaceEmbeddings(model_name="all-miniLM-L6-v2")  # all-miniLM-L6-v2(384) bge-large-en-v1.5(1024),  OpenAI text-embedding-3-small(1536), text-embedding-3-large(3072)
vectorstore = Chroma.from_documents(
    documents = splits,
    embedding = embeddings,
    persist_directory = CHROMA_DB #shutil.rmtree(CHROMA.DB)
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
 
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
 
query = "Show me the list of Machine learning related topics"
# query = "What are the furniture required in a class room environment"
response = rag_chain.invoke(query)
print(response)
 
# rag_chain = RunnableMap (context - vectorstore retrieved docs, input - user query, prompt_template, LLM, parser())
# response = rag_chain.invoke("tell me about java students list")
# print(response)
 
# Add this code at the end of your script to inspect the database:
 
# 1. Fetch data from Chroma DB (include both embeddings and document text)
db_data = vectorstore.get(include=["embeddings", "documents", "metadatas"])
 
# 2. Let's look at the very first chunk stored in the database (Index 0)
first_chunk_text = db_data["documents"][0]
first_chunk_vector = db_data["embeddings"][0]
first_chunk_metadata = db_data["metadatas"][0]
 
print("--- 📄 RAW TEXT CHUNK ---")
print(first_chunk_text)
print(f"\nSource Location: {first_chunk_metadata}")
 
print("\n--- 🔢 EMBEDDING VECTOR VALUE ---")
# Print the total number of dimensions (length of the list of numbers)
print(f"Vector Dimensions: {len(first_chunk_vector)}")
# Print just the first 10 numbers so it doesn't flood your screen
print(f"First 10 numbers of the vector: {first_chunk_vector[:10]}...")
 