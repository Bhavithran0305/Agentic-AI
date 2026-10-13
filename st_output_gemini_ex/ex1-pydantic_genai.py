"""import os
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

connect_client=genai.Client()

#json pydantic
class danticpy(BaseModel):
    name:str
    email: str
    phoneno:int
    skills:list[str]
    years_of_experience:int

response=connect_client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Tell me about Yourself!",
    config=genai.types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=500,
        response_mime_type="application/json",
        response_schema=danticpy
    )
)

print(response)
print("\n" + "=" * 60)



data= response.parsed # dict type
print("\n"+"="*60)
print(data)"""

# bug report Analyser
import os
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

client=genai.Client()

class BugReporter(BaseModel):
    BugTitle:str
    Severity:str
    Priority:str
    Affected_Module:str
    Reproduction_Steps:str

response=client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="in my webite i gets slow process of working, what was the reason it has in the behind!!",
    config=genai.types.GenerateContentConfig(
        #temperature=0.7,
        #max_output_tokens=500,
        response_mime_type="application/json",
        response_schema=BugReporter
    )
    
)
print(response)
print("\n" + "*"*100)
data=response.parsed
print(data)