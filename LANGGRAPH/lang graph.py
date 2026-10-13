import os
import re
from typing import TypedDict
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
# from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
 
 
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    # temperature=0.7
)
 
# llm2 = ChatDeepSeek(
#     model="deepseek-chat",
#     # temperature=0          
# )
class SimpleState(TypedDict):
    query: str
    category: str
    draft: str
    grade: int
    final: str
 
 
def classify(state: SimpleState):
    """ Decide if a query belongs to general or technical category """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in query classification. Return only the word 'technical' or 'general' based on the query. Do not return anything other than one of these words."),
        ("human", "{query}"),
    ])
    chain = prompt | llm | StrOutputParser()
    category = chain.invoke({"query": state['query']})
    print(f"Category: -----------   {category}")
    return {"category": category}
 
 
def general_answer(state: SimpleState):
    """ Return a precise answer for a general category query """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Give an unrefined, very short generic answer in a single sentence."),
        ("human", "{query}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({ "query": state['query']})
    print(f"GENERAL DRAFT : #######   {response}")
    return {"draft": response}
 
 
def technical_answer(state: SimpleState):
    """ Returns a technically detailed accurate answer for a technical category query """
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a technical assistant. Provide a very short one line technical answer."),
        ("human", "{query}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({ "query": state['query'] })
    print(f"TECH DRAFT: #######    {response}")
    return {"draft": response}
 
 
def grade_answer(state: SimpleState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in grading answers. Return only a single raw number from 1 to 10 based on the draft answer quality. If the answer is not detailed enough, give it a lower rating. Do not include markdown formatting, words, or punctuation."),
        ("human", "{draft}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({ "draft": state['draft'] })
    print(f"Grade :::::::::::: {response}")
    content = response
 
    if isinstance(content, list):
        content = " ".join(map(str, content))
 
    match = re.search(r'\d+', content) # the grading of this response is 7.
    grade_int = int(match.group()) if match else 1
 
    return {"grade": grade_int, "final": state["draft"]}
 
 
def polish(state: SimpleState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert editor. Expand the query draft answer into a detailed set of information with bullet points at the end highlighting major discussion points about the topic given."),
        ("human", "{draft}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({ "draft": state['draft'] })
    print(f" Polished Output : $$$$$$$$$$$       {response}")
    return {"final" : response}
 
 
def route_by_category(state: SimpleState):
    category_text = str(state["category"])
 
    if "technical" in category_text:
        return "technical_answer"
 
    return "general_answer"
 
 
def route_by_grade(state: SimpleState):
    return "polish" if state['grade'] < 8 else "__end__"
 
 
# Graph Configuration
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
 
# Execution Run
query_str = "what is the captial of australia"
response = graph.invoke({"query": query_str})
 
print("\n=== FINAL RESULT ===")
print(response.get("final"))
 
 