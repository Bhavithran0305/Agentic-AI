import os
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
 
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
 
agent = create_agent(
    model=llm,
    tools=[],
    middleware=[
        # Hash Email
        PIIMiddleware("email", strategy="hash"),
 
        # Block Credit Card
        PIIMiddleware("credit_card", strategy="block"),
    ],
)
 
# Example 1 (Email Hashing)
print("===== Example 1 =====")
 
text1 = """
Name: John
Email: john@gmail.com
"""
 
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": text1,
            }
        ]
    }
)
 
print(response["messages"][-1].content)
 
# Example 2 (Credit Card Blocking)
print("\n===== Example 2 =====")
 
text2 = """
Name: John
Email: john@gmail.com
Credit Card: 4111-1111-1111-1111
"""
 
try:
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": text2,
                }
            ]
        }
    )
 
    print(response["messages"][-1].content)
 
except Exception as e:
    print("Request Blocked!")
    print(e)
 





