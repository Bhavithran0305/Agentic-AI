"""[EX3:]Build a router: If the user asks about "Billing," go to the Billing Node; otherwise, go to the General
Support Node"""

import os 
import re
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()

key=os.getenv("DEEPSEEK_API_KEY")

bot=ChatOpenAI(
    model="deepseek-chat",
    api_key=key,
    base_url="https://api.deepseek.com"
)

class router_state(TypedDict):
    user_query:str
    classify:str
    routes:str
    
    

# Defining States
def get_category(state:router_state):
    prompt=ChatPromptTemplate.from_messages([
        ("system","You are good in classifying the router based on the query. Return only the word 'billing' or 'general_support' based on the user query. Do not return anyother which was not related to these two words"),
        ("human","{inputs}")
    ])
    chain=prompt|bot|StrOutputParser()
    response=chain.invoke({"inputs":state["user_query"]})
    print(f"--Router Classify--{response}")
    return{
        "classify":response
    }
def Billing_node(state:router_state):
    prompt=ChatPromptTemplate.from_messages([
        ("system","You are an Billing support assistant. Give the response if the query is related to a Billing details."),
        ("human","{inputs}")
    ])
    chain=prompt|bot|StrOutputParser()
    response=chain.invoke({"inputs":state["user_query"]})
    print(f"--BILLING NODE--{response}")
    return{
        "routes":response
    }
def General_Support_Node(state:router_state):
    prompt=ChatPromptTemplate.from_messages([
        ("system","You are an General Support Assistant. Give the response if the query related to General Customer Support details."),
        ("human","{inputs}")
    ])
    chain=prompt|bot|StrOutputParser()
    response=chain.invoke({"inputs":state["user_query"]})
    print(f"--General Support Node--{response}")
    return{
        "routes":response
    }
def custom_router(state:router_state):
    if "billing" in state["classify"]:
        return "Billing_node"
    return "General_Support_Node"

builder=StateGraph(router_state)
builder.add_node("classify",get_category)
builder.add_node("Billing_node",Billing_node)
builder.add_node("General_Support_Node",General_Support_Node)


builder.add_edge(START,"classify")
builder.add_conditional_edges("classify",custom_router,
    {
        "Billing_node":"Billing_node",
        "General_Support_Node":"General_Support_Node"
    }
)
builder.add_edge("Billing_node",END)
builder.add_edge("General_Support_Node",END)

graph=builder.compile()

#inputs="give the invoice details of this billing."
inputs="What is the procedure to change the username and password."
response=graph.invoke({"user_query":inputs})
print("\n--Final Response--\n")
print(response.get("routes"))
