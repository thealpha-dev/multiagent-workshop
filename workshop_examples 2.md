# Multi-Agent Systems Workshop Examples

This document provides additional examples and code snippets to supplement the workshop on Multi-Agent Systems. These examples can be used to demonstrate various concepts and frameworks during the workshop or as follow-up exercises for participants.

## Table of Contents

1. [Basic LangChain Agent](#basic-langchain-agent)
2. [Multi-Agent Conversation with LangGraph](#multi-agent-conversation-with-langgraph)
3. [AutoGen Multi-Agent System](#autogen-multi-agent-system)
4. [CrewAI Example](#crewai-example)
5. [Advanced Agent with Memory](#advanced-agent-with-memory)

## Basic LangChain Agent

This example creates a simple agent that can use Wikipedia to answer questions.

```python
import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Initialize the LLM
llm = ChatOpenAI(temperature=0)

# Initialize the Wikipedia tool
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
tools = [wikipedia]

# Define the prompt template for the agent
prompt_template = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you want to answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
""")

# Create the agent
agent = create_react_agent(llm, tools, prompt_template)

# Create the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent
print(agent_executor.invoke({"input": "What is the capital of France?"}))
print(agent_executor.invoke({"input": "Who is the current president of the United States?"}))
```

## Multi-Agent Conversation with LangGraph

This example demonstrates how to create a simple multi-agent system using LangGraph where agents can communicate with each other.

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import Dict, List, Annotated, TypedDict

# Define the state
class AgentState(TypedDict):
    messages: List[str]
    next_agent: str

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Create the researcher agent
researcher_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research agent. Your job is to find information about topics and provide detailed facts."),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])
researcher_chain = researcher_prompt | llm

# Create the writer agent
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a writer agent. Your job is to take research and create well-written, engaging content."),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])
writer_chain = writer_prompt | llm

# Create the editor agent
editor_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an editor agent. Your job is to improve and refine content, checking for clarity, grammar, and style."),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{input}")
])
editor_chain = editor_prompt | llm

# Define agent nodes
def researcher_node(state):
    messages = state["messages"]
    response = researcher_chain.invoke({"messages": messages, "input": messages[-1].content})
    return {"messages": messages + [response], "next_agent": "writer"}

def writer_node(state):
    messages = state["messages"]
    response = writer_chain.invoke({"messages": messages, "input": messages[-1].content})
    return {"messages": messages + [response], "next_agent": "editor"}

def editor_node(state):
    messages = state["messages"]
    response = editor_chain.invoke({"messages": messages, "input": messages[-1].content})
    return {"messages": messages + [response], "next_agent": "end"}

# Define the router
def router(state):
    return state["next_agent"]

# Create the graph
workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)
workflow.add_node("editor", editor_node)

# Add edges
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "editor")
workflow.add_edge("editor", END)

# Set the entry point
workflow.set_entry_point("researcher")

# Compile the graph
chain = workflow.compile()

# Run the multi-agent system
result = chain.invoke({
    "messages": [HumanMessage(content="Write a short article about multi-agent systems in AI.")],
    "next_agent": "researcher"
})

# Print the conversation
for message in result["messages"]:
    print(f"{message.type}: {message.content}\n")
```

## AutoGen Multi-Agent System

This example demonstrates a multi-agent system using Microsoft's AutoGen framework, featuring a user proxy agent, an assistant agent, and a code execution agent.

```python
import autogen

# Configure the LLM
config_list = [
    {
        "model": "gpt-3.5-turbo",
        "api_key": "your-api-key-here"
    }
]

# Create the assistant agent
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"config_list": config_list},
    system_message="You are a helpful AI assistant. You can help with tasks, answer questions, and generate code when needed."
)

# Create the coder agent
coder = autogen.AssistantAgent(
    name="coder",
    llm_config={"config_list": config_list},
    system_message="You are an expert Python programmer. You write clean, efficient, and well-documented code to solve problems."
)

# Create the user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: "TASK COMPLETE" in x.get("content", ""),
    code_execution_config={"work_dir": "coding", "use_docker": False},
)

# Create a group chat
groupchat = autogen.GroupChat(
    agents=[user_proxy, assistant, coder],
    messages=[],
    max_round=12
)

# Create the group chat manager
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
)

# Start the conversation
user_proxy.initiate_chat(
    manager,
    message="I need to analyze a dataset of student grades and create a visualization showing the distribution. Can you help me write a Python script for this?"
)
```

## CrewAI Example

This example demonstrates how to create a research crew using CrewAI to analyze a topic and generate a report.

```python
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# Initialize the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

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
```

## Advanced Agent with Memory

This example demonstrates how to create an agent with memory capabilities using LangChain.

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.memory import ConversationBufferMemory

# Initialize the LLM
llm = ChatOpenAI(temperature=0)

# Initialize the search tool
search = DuckDuckGoSearchRun()
tools = [search]

# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the prompt template with memory
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant with access to the following tools: {tools}. Use them to answer the user's questions."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create the agent executor with memory
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Run the agent with memory
print(agent_executor.invoke({"input": "What is the capital of France?"}))
print(agent_executor.invoke({"input": "What is the population of that city?"}))
print(agent_executor.invoke({"input": "Tell me about its famous landmarks."}))
```

## Additional Resources

For more examples and detailed documentation, refer to the following resources:

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AutoGen GitHub Repository](https://github.com/microsoft/autogen)
- [CrewAI Documentation](https://docs.crewai.com/introduction)

These examples provide a starting point for exploring multi-agent systems using different frameworks. Feel free to modify and extend them to suit your specific needs and use cases.

