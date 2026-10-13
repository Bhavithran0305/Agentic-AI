"""
#This program works if you provide the api key in the .env file
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()
 
client = genai.Client()
    
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Explain why the sky is blue in one sentence."
)
 
print(response)
print("*" * 150)
print(response.text)
 


 """
import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

client=genai.Client()

query="tell me a joke!"

response=client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=query
)

print(response)
print("*"*100)
print(response.text)