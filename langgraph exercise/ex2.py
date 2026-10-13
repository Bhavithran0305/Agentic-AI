"""[EX.2]:Define a custom "State" object that tracks a user's name and their "Current Mood" throughout a graph
execution.
"""
import os
import re
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

bot=ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite"
)

class State(BaseModel):
    name:str
    mood:str

#Custom States
def get_name(state:State):
    prompts=ChatPromptTemplate.from_messages([
        ("system","You are an helpful assistant."),
        ("human","{name}")
    ])
    chain=prompts|bot|StrOutputParser()
    response=chain.invoke({"name":state.name})
    print(f"**NAME**{response}")
    return{
        "name":state.name
        
    }
def get_current_mood(state:State):
    prompts=ChatPromptTemplate.from_messages([
        ("system","Your are an helpful assistant"),
        ("human","{mood}, Encourage the user based on the mood type.")
    ])
    chain=prompts|bot|StrOutputParser()
    response=chain.invoke({"mood":state.mood})
    print(f"**CURRENT_MOOD**{response}")
    return{
        "mood":state.mood
    }
#graph building

workflow=StateGraph(State)
workflow.add_node("name",get_name)
workflow.add_node("mood",get_current_mood)

workflow.add_edge(START,"name")
workflow.add_edge("name","mood")
workflow.add_edge("mood",END)

graph=workflow.compile()
response=graph.invoke({
    "name":input("Enter the name: "),
    "mood":input("Enter the mood: ")
})
print(response)

