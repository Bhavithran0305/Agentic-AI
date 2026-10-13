
# [1]: Basic --> llm
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI #from google import genai
from langchain_core.output_parsers import StrOutputParser #
from langchain_core.prompts import ChatPromptTemplate
   
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.7
)
 
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant"),
    ("user", "write a small poem about {title} ")
])
 
chain = prompt |llm # StrOutputParser()  #commaseperatedlistoutputparser
 
print("Sending request to Gemini...\n")
response = chain.invoke({"title":input("enter the title:")})
 
print("--- Gemini Response ---")
#print(response.text) this line is not needed for the langchain conncetors in the stroutputparser because the connector will 
#convert the ai messages into plain text..
print(response)
print("*"*60)
print(response.text)

