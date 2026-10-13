# Parallel
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableParallel
from dotenv import load_dotenv
load_dotenv()

bot=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.7
)
rp_task=ChatPromptTemplate.from_template("name of the movie is {movie}")
rp_chain= rp_task|bot|StrOutputParser()

rp_task_1=ChatPromptTemplate.from_messages([
    ("system","Your an kollywood movie reviewer ai assistant"),
    ("human","give  detailed description about the movie  {name}")
])
chain_1= rp_task_1|bot|StrOutputParser()

rp_task_2=ChatPromptTemplate.from_messages([
    ("system","Your an kollywod movie reviewer ai assistant"),
    ("human","give the detailed descripiton about the hero of the movie: {name}")
])
chain_2=rp_task_2|bot|StrOutputParser()


rp_final_task=(rp_chain|{"name": RunnablePassthrough()}| RunnableParallel({
    "task1":chain_1,
    "task2":chain_2
}))


response=rp_final_task.invoke({"movie":{input("enter the name:")}})
print(response["task1"])
print(response["task2"])