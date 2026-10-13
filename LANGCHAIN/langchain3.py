#[3]: Basic --> LLM --> StrOutputParser() --> CommaSeparatedListOutputParser()
                                                              
#importing require libraries
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

#connecting llm model
bot=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=1.2
)
#creating prompts using ChatPromptTemplate
prompts=ChatPromptTemplate.from_template("List out the names of tamilnadu {name}")

# langchain connections
lang_chain= prompts | bot| StrOutputParser() |CommaSeparatedListOutputParser()
print(lang_chain.invoke({"name":input("enter the name: ")}))

print(lang_chain)
print("--"*25)
print(type(lang_chain))
#print("**"*25)
#print(type(StrOutputParser()))




