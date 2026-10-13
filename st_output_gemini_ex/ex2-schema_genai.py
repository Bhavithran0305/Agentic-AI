"""import os
from google import genai
import json
from dotenv import load_dotenv
load_dotenv()

connect_client=genai.Client()

#json schema
schema={
    "type":"object",
    "properties":{
        "Name":{"type":"string"},
        "Email":{"type":"string"},
        "PhoneNo":{"type":"integer"},
        "Skills":{
            "type":"array",
            "items":{"type":"string"}
        },
        "Years of Experience":{"type":"integer"},
    },
    "required":["Name","Email","PhoneNo","Skills","Years of Experience"]
}
response=connect_client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Tell me about Yourself!",
    config=genai.types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=500,
        response_mime_type="application/json",
        response_schema=schema
    )
)

print(response)
print("\n" + "=" * 60)

print(response.text) #json type

data=json.loads(response.text) # dict type
print("\n"+"="*60)
print(data)"""

# customer Support ticketer classification

import os
from google import genai
import json
from dotenv import load_dotenv
load_dotenv()

client=genai.Client()

Customer_Support={
    "type":"object",
    "properties":{
        "Category":{"type":"string"},
        "Priority":{"type":"string"},
        "Sentiment":{"type":"string"},
        "Assigned Department":{"type":"string"}
    },
    "required":["Category","Priority","Sentiment","Assigned Department"]
}

response=client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="I booked the ticket for a movie due to some personal issue i didn't go to the movie,can you give the procedure to reshare the money of the ticket!",
    config=genai.types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=500,
        response_mime_type="application/json",
        response_schema=Customer_Support

    )
    

)
print(response)
print("\n"+"*"*60)

print(response.text)
print("\n"+"*"*60)

data=json.loads(response.text)
print(data,"\n"),


print("*"*60)
print("Category",data['Category'])
print("Priority",data['Priority'])

