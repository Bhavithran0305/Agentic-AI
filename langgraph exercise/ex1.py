
"""[EX.1]:Create a 2-node graph where Node A "Cleans" the user input and Node B "Responds"""

import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

#defining the llm model
bot=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

# defining the states 
class Starting_state(TypedDict):
    user_query:str #starting state
    Node_A:str  # Node_A refers to Clean input
    Node_B:str # Node_B refers to giving the response to the clean input
    

def first_node(state:Starting_state):
    """this first node gives the clean input of the user query"""
    prompts=ChatPromptTemplate.from_messages([
        ("system","Your an intelligent AI assistant, your work is to get the user input and "
        "convert  that into  'Clean input' and send  to the Node_B(second_node)"),
        ("human","{query}")
    ])
    linking=prompts|bot|StrOutputParser()
    Node_A=linking.invoke({"query":state["user_query"]})
    print(f"Node-A**********{Node_A}")
    return{"Node_A":Node_A}

def second_node(state:Starting_state):
    """ this node is to give respond for the previous clean input that is from Node A"""
    prompts=ChatPromptTemplate.from_messages([
        ("system","You are an helpful assistant, give the respond when the Node_A(first_node) gives you the clean input "),
        ("human","{query}")
    ])
    linking=prompts|bot|StrOutputParser()
    Node_B=linking.invoke({"query":state["Node_A"]})
    print(f"Responds**********{Node_B}")
    return{"Node_B":Node_B}

#Graph Configuration
builder=StateGraph(Starting_state)
builder.add_node("Node_A",first_node)
builder.add_node("Node_B",second_node)

builder.add_edge(START,"Node_A")
builder.add_edge("Node_A","Node_B")
builder.add_edge("Node_B",END)


graph=builder.compile()

#user query
question=input("enter the querry: ")
response=graph.invoke({"user_query":question})
print("---Final Response---")
print(response.get("Node_B"))
