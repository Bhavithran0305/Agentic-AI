"""Build a two-agent team: 
One agent "Researches" a topic and 
the second "Summarizes" it into a bulleted list."""

import os
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew, LLM

gemini_bot=LLM(
    model="gemini/gemini-3.1-flash-lite",
    temperature=0.2
)

searching_tool=SerperDevTool()
"""defining the roles of the agents"""
# first agent

Researcher_agent=Agent(
    role="Current affairs Researcher",
    goal="Research about the user query :  {query}",
    backstory=(
        "You are an expert in researching. Your an current affairs researcher, where you have all the"
        "detatils that happens in the present dates and in the past dates."
    ),
    tools=[searching_tool],
    llm=gemini_bot,
    max_rpm=10,
    verbose=True
)

# second agent

Editor_agent=Agent(
    role="Editing the Researcher",
    goal="editing the result of the {query} from the  Researcher Agent",
    backstory=(
        "You are very specialized agent in the field of editing. You take result from the"
        "Researcher_agent and polish that researches by fixing the grammatical mistakes,"
        "correct sentence formation, result deliverying,etc,."
    ),
    tools=[searching_tool],
    llm=gemini_bot,
    max_rpm=10,
    verbose=True
)

# third agent
Summarizing_agent=Agent(
    role="Summarizzing the editing result",
    goal="Sumarizing the final result into an bullet points",
    backstory=(
        "Your work is to summarize the important context from the result of the Editor_agent."    
    ),
    tools=[searching_tool],
    llm=gemini_bot,
    max_rpm=10,
    verbose=True
)

"""defining the task for the agents"""
# first task
Researcher_task=Task(
    agent=Researcher_agent,
    description=(
        "Your task is to research the details of the  current affairs based on the th user query : {query}"
        "and give its full details."
    ),
    expected_output="The output should have the detailed and lenghtier explanation of the topic in a single passage "
    "and give the result should be in less than 700 words and not go beyond that. " 
    "In the end mention the number of words used."
)

# second task

Editor_task=Task(
    agent=Editor_agent,
    description=(
        "Your task is to getting the result from the Researcher_task and do the editing of that result. The editing"
        "task is that polish the details of the Resercher_task by correcting the grammatical errors and sentence formation."
        "Edit the result by providing the information in an consice way of deliverying."
    ),
    expected_output="The output should have four sections. 'Section-1' is Introduction, Section-2 is Features, Section-3 is"
    "Advantage and Disadvantage and Section-4 is Conclusion. Maintain the range of words within 300 words."
    " In the end of the result mention the number of words used."
)

# third task

Summarizing_task=Task(
    agent=Summarizing_agent,
    description=(
        "Your task is to sumarize the result from the Editor_task of bringing the top 5 important points"
        "from each section of the Editor_task. Tose 5 points should be in the single line statement"
    ),
    expected_output="The 5 important points from each sections should have only one line in each points." \
    "Give those points in the bullet points."
)

"""defining the crew"""

#crew task
components_crew=Crew(
    agents=[Researcher_agent,Editor_agent,Summarizing_agent],
    tasks=[Researcher_task,Editor_task,Summarizing_task]
)

topic={"query": "Impacts of AI in IT industry in the year of 2026."}
response=components_crew.kickoff(inputs=topic)
print("---FINAL CREW TASK---")

print(response)
