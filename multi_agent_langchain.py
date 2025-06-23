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
llm = ChatOpenAI(
    openai_api_key="sk-0ca52251e80a4324b67b9834cc468de7",
    openai_api_base="https://thealpha.dev/api",
    model_name="thealphadev",
    temperature=0)

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