import os
from dotenv import load_dotenv
load_dotenv()
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew, LLM
 
gemini_llm = LLM(
    model="gemini/gemini-3.1-flash-lite",
    temperature=0.2
)
 
search_tool = SerperDevTool()
 
researcher = Agent(
    role="Kollywood Movie Reviewer",
    goal="Review the movie base on the user {topic} .",
    backstory=(
        "You are an expert in reviewing the movie. You have a specialized knowledge in"
        "the concept of movies of kollywood in the field of story, direction, cinemotography,"
        "background-music,etc,."
    ),
    tools=[search_tool],
    llm=gemini_llm,
    #max_rpm=15,
    verbose=True
)
 
writer = Agent(
    role="Movie Improvisor",
    goal="Giving the suggestions to improvise the movie",
    backstory=(
        "You are the top-class movie improviser in the universe.Your movies are having feel good flims,"
        "action flims, biography flims,etc,. The flims in your direction was top-class which makes the audience"
        "to feel good for the purchasing of the ticket."
    ),
    llm=gemini_llm,
    #max_rpm=15,
    verbose=True
)
 
research_task = Task(
    description=(
        "Review the movie based on the user givesthe name{topic}."
    ),
    expected_output="A bulleted list of raw mistakes in the movie, key metrics, and its insights.",
    agent=researcher
)
 
writing_task = Task(
    description=(
        "Using the result of the research review from the Kollywood Movie reviewer"
        "improvise the movie as per your services and give how to improve the mistakess from the"
        "review of the Kllywood Movie Reviewer"
    ),
    expected_output="A top-class movie improvising, roughly 300-500 words.",
    agent=writer,
)
 
market_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task]
)
 
title = {"topic": "Kadaikutty Singam"}
result = market_crew.kickoff(inputs=title)
 
print("\n#### CREW TASK COMPLETE ####\n")
print(result)
 