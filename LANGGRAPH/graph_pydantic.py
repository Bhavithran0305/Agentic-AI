import os
import re
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
 
# LLM Configurations
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.7
)
 
# Pydantic State Schema
class SimpleState(BaseModel):
    query: str
    title: str # Provide defaults so graph initialization doesn't complain about missing keys
    draft: str
    grade: int
    final: str
 
# --- Nodes ---
 
def classify(state: SimpleState):
    """ Decide if a query belongs to general or technical category """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in query classification. Return only the word 'technical' or 'general' based on the query. Do not return anything other than one of these words."),
        ("human", "{query}"),
    ])
    cl_chain = prompt | llm | StrOutputParser()
    # FIX: Changed state['query'] to state.query
    cl_category = cl_chain.invoke({"query": state.query})
   
    print(f"Category: -----------   {cl_category}")
    return {"title": cl_category}
 
 
def general_answer(state: SimpleState):
    """ Return a precise answer for a general category query """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Give an unrefined, very short generic answer in a single sentence."),
        ("human", "{query}")
    ])
    g_chain = prompt | llm | StrOutputParser()
    # FIX: Changed state['query'] to state.query
    g_response = g_chain.invoke({ "query": state.query})
    print(f"GENERAL DRAFT : #######   {g_response}")
    return {"draft": g_response}
 
 
def technical_answer(state: SimpleState):
    """ Returns a technically detailed accurate answer for a technical category query """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical assistant. Provide a very short one line technical answer."),
        ("human", "{query}")
    ])
    t_chain = prompt | llm | StrOutputParser()
    # FIX: Changed state['query'] to state.query
    t_response = t_chain.invoke({ "query": state.query })
    print(f"TECH DRAFT: #######    {t_response}")
    return {"draft": t_response}
 
 
def grade_answer(state: SimpleState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in grading answers. Return only a single raw number from 1 to 10 based on the draft answer quality. If the answer is not detailed enough, give it a lower rating. Do not include markdown formatting, words, or punctuation."),
        ("human",  "{draft}")
    ])
    chain = prompt | llm | StrOutputParser()
    # FIX: Changed state['draft'] to state.draft
    content = chain.invoke({ "draft": state.draft })
    print(f"Grade :::::::::::: {content}")
 
    match = re.search(r'\d+', content)
    grade_int = int(match.group()) if match else 1
 
    return {"grade": grade_int}
 
 
def polish(state: SimpleState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert editor. Expand the query draft answer into a detailed set of information with bullet points at the end highlighting major discussion points about the topic given."),
        ("human", "{draft}")
    ])
    chain = prompt | llm | StrOutputParser()
    # FIX: Changed state['draft'] to state.draft
    response = chain.invoke({ "draft": state.draft })
    print(f" Polished Output : $$$$$$$$$$$       {response}")
    return {"final" : response}
 
# --- Routing Logic ---
 
def route_by_category(state: SimpleState):
    # FIX: Changed state["title"] to state.title
    if "technical" in state.title.lower():
        return "technical_answer"
    return "general_answer"
 
 
def route_by_grade(state: SimpleState):
    # FIX: Changed state['grade'] to state.grade
    return "polish" if state.grade < 8 else "__end__"
 
 
# --- Graph Configuration ---
builder = StateGraph(SimpleState)
builder.add_node("classify", classify)
builder.add_node("general_answer", general_answer)
builder.add_node("technical_answer", technical_answer)
builder.add_node("grade_answer", grade_answer)
builder.add_node("polish", polish)
 
builder.add_edge(START, "classify")
 
builder.add_conditional_edges("classify", route_by_category,
    {
        "technical_answer": "technical_answer",
        "general_answer": "general_answer"
    }
)
builder.add_edge("general_answer", "grade_answer")
builder.add_edge("technical_answer", "grade_answer")
 
builder.add_conditional_edges("grade_answer", route_by_grade,
    {
        "polish": "polish",
        "__end__": END
    }
)
builder.add_edge("polish", END)
 
graph = builder.compile()
 
# --- Execution Run ---
query_str = "what is machine learning and its types?"
response = graph.invoke({"query": query_str})
 
# print("\n=== FINAL RESULT ===")
# print(response)
 
 
print("\n=== FINAL RESULT ===")
# Use dictionary lookup since LangGraph returns the final state as a dict
if response.get("final"):
    print(response.get("final"))
else:
    print(f"Skipped polish (Grade: {response.get('grade')}).\nResult: {response.get('draft')}")
























 
 