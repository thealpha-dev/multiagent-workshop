from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Initialize the LLM
llm = ChatOpenAI(
    openai_api_key="api-key",
    openai_api_base="https://thealpha.dev/api",
    model_name="thealphadev",
    temperature=0.7)

# Create the agents
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover comprehensive and accurate information about the assigned topic",
    backstory="You are an experienced research analyst with a keen eye for detail and a talent for finding obscure but valuable information.",
    verbose=True,
    llm=llm
)

writer = Agent(
    role="Content Strategist and Writer",
    goal="Create engaging, informative content based on research findings",
    backstory="You are a skilled writer who can transform complex research into compelling narratives that engage and inform readers.",
    verbose=True,
    llm=llm
)

editor = Agent(
    role="Editorial Director",
    goal="Ensure content accuracy, clarity, and adherence to high editorial standards",
    backstory="You have years of experience in publishing, with a sharp eye for detail and a commitment to editorial excellence.",
    verbose=True,
    llm=llm
)

# Create the tasks
research_task = Task(
    description="Research the topic of 'Multi-Agent Systems in AI' thoroughly. Identify key concepts, recent developments, major frameworks, and notable applications.",
    expected_output="A comprehensive research document with well-organized findings, including key points, trends, and specific examples.",
    agent=researcher
)

writing_task = Task(
    description="Using the research provided, create an engaging and informative article about Multi-Agent Systems in AI. The article should explain concepts clearly, highlight practical applications, and discuss future trends.",
    expected_output="A well-structured article of approximately 1000 words that effectively communicates the topic to a technical audience.",
    agent=writer,
    context=[research_task]
)

editing_task = Task(
    description="Review and refine the article for clarity, accuracy, and engagement. Ensure all technical concepts are explained correctly, the structure is logical, and the writing is engaging.",
    expected_output="A polished final article ready for publication, with any issues in the original draft resolved.",
    agent=editor,
    context=[writing_task]
)

# Create and run the crew
crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, writing_task, editing_task],
    verbose=2
)

result = crew.kickoff()
print(result)