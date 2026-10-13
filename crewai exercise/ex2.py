"""Build a "Comparison Bot" that asks 3 different models the same question at
 the same time and summarizes the best parts of each."""

import os 
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import SerperDevTool
from crewai import Agent,Task,Crew,LLM

gemini_bot=LLM(
    model="gemini/gemini-3.1-flash-lite",
    temperature=0.2
)
deepseek_bot=LLM(
    model="deepseek/deepseek-chat",
    temperature=0.2
)
searching_tools=SerperDevTool()

# GEMINI MODEL

gemini_agent=Agent(
    role="Maths Professor",
    goal="Teach the mathematical concepts and problems given:{problem}",
    backstory=(
        "You have done PhD in Mathematics, you have the ability to solve the problems and have teaching"
        "skills to explain all the concepts related to mathematics to others easily and in an consicely."
    ),
    tools=[searching_tools],
    llm=gemini_bot,
    max_rpm=10,
    verbose=True
)

gemini_task=Task(
    agent=gemini_agent,
    description=(
        "You have to teach the mathematical topics and then solve the given problem{problem}. The problem" \
         "should be exactly solved within 5 steps and not to go beyond that."
    ),
    expected_output="In the output it should have the problem 'METHODS','PROPERTIES','FORMULAS' after giving thes" \
    "solve the problem or teach the concept based on the problem given:{problem}"
)
gemini_crew=Crew(
    agents=[gemini_agent],
    tasks=[gemini_task]
)

#DEEPSEEK MODEL
deepseek_agent=Agent(
    role="Maths Professor",
    goal="Teach the mathematical concepts and problems given:{problem}",
    backstory=(
        "You have done PhD in Mathematics, you have the ability to solve the problems and have teaching"
        "skills to explain all the concepts related to mathematics to others easily and in an consicely."
    ),
    tools=[searching_tools],
    llm=deepseek_bot,
    max_rpm=10,
    verbose=True
    )

deepseek_task=Task(
    agent=deepseek_agent,
    description=(
        "You have to teach the mathematical topics and then solve the given problem{problem}. The problem" \
        "should be exactly solved within 5 steps and not to go beyond that."
    ),
    expected_output="In the output it should have the problem 'TOPIC','METHODS','PROPERTIES','FORMULAS' after giving thes" \
    "solve the problem or teach the concept based on the problem given:{problem}"
    )
deepseek_crew=Crew(
    agents=[deepseek_agent],
    tasks=[deepseek_task]
)

#COMPARISON MODEL

comparison_agent=Agent(
    role="Comparison Agent",
    goal="Run the two model simulatneously and summarize the best part of each",
    backstory=(
        "This agent compares the two model then find which model has given the perfect response for the user query " \
        "and then summarize the best part of each model response."
    ),
    llm=gemini_bot,
    verbose=True
)
comparison_task=Task(
    agent=comparison_agent,
    description=(
        "The task given is that you have to run the two model the gemini_bot and deepseek_bot at the same time for the same user question," \
        "after the response compare both the response of the model and give which one has the perfect response and then give the summarize the" \
        "best part of response in each model. "
    ),
    expected_output="The output should have shown in the table format, where it has these required fields score them out of 10"
    "for each fields. The fields are:"
    "1.MODEL ACCURACY"
    "2.MODEL PREDICTION"
    "3.WHICH MODEL HAS GIVEN THE FASTEST RESPONSE"
    "4.DATA USAGE"
    "5.TOTAL SCORE"
    "Based on the final  gained by each model give who is the winner. Then summarize the best " \
    "part of each response of the model."
)

comparison_crew=Crew(
    agents=[comparison_agent],
    tasks=[comparison_task]
)

query={"problem":"You roll two normal dice at the same time. One die is red and the other die is blue."
        "Each die has numbers from 1 to 6. What is the chance that the top numbers on both dice add up to 8?"}


print("****GEMINI MODEL RESPONSE*****")
response_1=gemini_crew.kickoff(inputs=query)
print(response_1)

print("****DEEPSEEK MODEL RESPONSE*****")
response_2=deepseek_crew.kickoff(inputs=query)
print(response_2)

print("****COMPARISON BOT*****")
final_response=comparison_crew.kickoff(inputs={
    "problem":query["problem"],
    "gemini": str(response_1),
    "deepseek":str(response_2)
})

print("****COMPARISON CREW TASK****")
print(final_response)






