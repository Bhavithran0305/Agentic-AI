import os
from langfuse.openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
 
 
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
 
def generate_response():
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "you are helpful assistant"},
            {"role": "user", "content": "what is quantam computing "}
        ],
        # name given to the Langfuse's wrapper
        name="chat",
 
        # metadata for the chat history
        metadata={
            "langfuse_session_id": "user2"
        }
    )
   
    return response.choices[0].message.content
 
# Example usage:
print(generate_response())