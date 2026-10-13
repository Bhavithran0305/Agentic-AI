import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("DEEPSEEK_API_KEY")
 
bot = ChatOpenAI(
    model="deepseek-chat",
    api_key=key,
    base_url="https://api.deepseek.com"
)
rp_task=ChatPromptTemplate.from_template("What is the formula for Volume of  {name}")
rp_chain= rp_task|bot|StrOutputParser()

rp_task_1=ChatPromptTemplate.from_template("What is the formula for Area of : {topic}")
chain_1= rp_task_1|bot|StrOutputParser()

rp_task_2=ChatPromptTemplate.from_template("What is the formula for Perimeter of :{topic}")
chain_2=rp_task_2|bot|StrOutputParser()


response=rp_chain.invoke({"name":{input("enter the name:")}})
Translation=RunnableParallel(
    t1=chain_1,
    t2=chain_2
).invoke({"topic":{input("enter the name:")},"topic":response})
print(response)
print("**"*25)
print("*** Area***\n")
print(Translation["t1"])
print("**Perimete**\n")
print("**"*25)
print(Translation["t2"])