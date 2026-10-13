import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START,END
from typing import TypedDict

llm=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)
#STATES
class lang_states(TypedDict):
    Node_1:str
    Node_2:str

#first_state
def first_state(state:lang_states):
    prompts=ChatPromptTemplate.from_messages(
        ("system","Your an helpful AI assistant!"),
        ("user","{query}")
    )
    chain=prompts|llm|StrOutputParser()
    Node_1=chain.invoke({"query":state["Node_1"]})
    print("node_1")
    return Node_1

#second state

def second_state(state:lang_states):
    prompts=ChatPromptTemplate.from_messages(
           ("system","You have to simply print this  when no query is"
           "passed 'This is a rag Process'"),
           ("user","{query}")
       )
    chain=prompts|llm|StrOutputParser()
    Node_2=chain.invoke({"query":state["Node_2"]})
    print("node_2")
    return Node_2

builder=StateGraph(lang_states)
builder.add_node("Node_1",first_state)
builder.add_node("Node_2",second_state)

builder.add_edge(START,"Node_1")
builder.add_edge("Node_1","Node_2")
builder.add_edge("Node_2",END)

graph=builder.compile()

promt="what is an AI?"
response=graph.invoke(promt)
print(response)




