
# [2]: basic --> llm --> StrOutput() 
# importings
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
# sending request to llm that here it is defined as bot!
bot= ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=1.2
)
#giving prompts
prompts=ChatPromptTemplate.from_messages([
    ("system","You are a mathematical AI assistant give answer or response only from the mathematical subject"),
    ("human","What is the prime minister of {topic}")
])      
""" the **from_messages** is need to defined the response both system and the user to the llm!
if we want to defined only the user response to get the result for general question we use ** from_template**"""
# conecting the langchain

chain=prompts|bot|StrOutputParser() # gives the ai messages into a plain text!

# triggering for the results

print("** Gemini Response**\n")
response=chain.invoke({"topic":input("enter the topic")})

print("---Final Result---\n")
print(response)

