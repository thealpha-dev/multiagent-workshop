# Hands-on Exercises: Multi-Agent Systems Workshop

This document provides structured exercises for workshop participants to practice building and working with multi-agent systems. These exercises progress from basic to more advanced concepts.

## Exercise 1: Basic Agent Creation

**Objective:** Create a simple agent that can answer questions using a search tool.

**Instructions:**

1. Set up your environment as shown in the workshop:
   ```bash
   python3 -m venv venv_mas
   source venv_mas/bin/activate  # On Windows: .\venv_mas\Scripts\activate
   pip install langchain langchain_openai wikipedia
   ```

2. Create a file named `basic_agent.py` with the code from the workshop slides.

3. Modify the agent to use a different tool:
   - Replace the Wikipedia tool with a calculator tool
   - Test the agent with mathematical questions

4. **Challenge:** Add error handling to your agent to gracefully handle cases where the tool fails.

## Exercise 2: Multi-Agent Collaboration

**Objective:** Create a simple multi-agent system where agents collaborate to solve a problem.

**Instructions:**

1. Install the necessary packages:
   ```bash
   pip install langgraph
   ```

2. Create a file named `multi_agent.py` with the following structure:

   ```python
   from langchain_openai import ChatOpenAI
   from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
   from langchain_core.messages import HumanMessage, AIMessage
   from langgraph.graph import StateGraph, END
   from typing import Dict, List, Annotated, TypedDict
   
   # Define your state
   class AgentState(TypedDict):
       messages: List
       next_agent: str
   
   # Initialize the LLM
   llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
   
   # TODO: Create your agents here
   
   # TODO: Define agent nodes
   
   # TODO: Create the graph
   
   # TODO: Run the multi-agent system
   ```

3. Complete the code to create a system with three agents:
   - A researcher agent that gathers information
   - An analyst agent that processes and analyzes the information
   - A presenter agent that formats the results for presentation

4. Test your system with the query: "Analyze the impact of multi-agent systems on software development."

5. **Challenge:** Add a supervisor agent that can decide which agent should act next based on the current state.

## Exercise 3: Tool-Using Agents

**Objective:** Create an agent that can use multiple tools to solve complex problems.

**Instructions:**

1. Install additional packages:
   ```bash
   pip install langchain_community
   ```

2. Create a file named `tool_agent.py` with a structure similar to the basic agent.

3. Add the following tools to your agent:
   - A search tool (e.g., DuckDuckGoSearchRun)
   - A calculator tool
   - A weather tool (you can mock this with a simple function)

4. Create a prompt that instructs the agent to use the appropriate tool based on the question.

5. Test your agent with questions that require different tools:
   - "What is the capital of Japan?"
   - "What is 234 * 456?"
   - "What's the weather like in New York today?" (This will use your mock function)

6. **Challenge:** Add a tool that allows the agent to write content to a file, and have it save its research findings.

## Exercise 4: Agent with Memory

**Objective:** Create an agent that can remember previous interactions and maintain context.

**Instructions:**

1. Modify your basic agent to include a ConversationBufferMemory:
   ```python
   from langchain.memory import ConversationBufferMemory
   
   memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
   
   # Update your prompt to include the memory
   prompt = ChatPromptTemplate.from_messages([
       ("system", "You are a helpful assistant."),
       MessagesPlaceholder(variable_name="chat_history"),
       ("human", "{input}"),
       MessagesPlaceholder(variable_name="agent_scratchpad")
   ])
   
   # Create the agent executor with memory
   agent_executor = AgentExecutor(
       agent=agent,
       tools=tools,
       memory=memory,
       verbose=True
   )
   ```

2. Test your agent with a series of related questions:
   - "What is the capital of France?"
   - "What is the population of that city?"
   - "Tell me about its famous landmarks."

3. **Challenge:** Implement a different memory type, such as ConversationSummaryMemory, and compare how it affects the agent's responses.

## Exercise 5: CrewAI Implementation

**Objective:** Create a multi-agent system using CrewAI to solve a complex task.

**Instructions:**

1. Install CrewAI:
   ```bash
   pip install crewai
   ```

2. Create a file named `crew_system.py` with the following structure:

   ```python
   from crewai import Agent, Task, Crew
   from langchain_openai import ChatOpenAI
   
   # Initialize the LLM
   llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
   
   # TODO: Create your agents
   
   # TODO: Create your tasks
   
   # TODO: Create and run your crew
   ```

3. Complete the code to create a crew with at least three agents:
   - A researcher agent
   - A data analyst agent
   - A report writer agent

4. Define tasks for each agent that contribute to analyzing a dataset and creating a report.

5. Test your crew with the task: "Analyze the trends in AI research over the past five years."

6. **Challenge:** Add a reviewer agent that provides feedback on the report and suggests improvements.

## Exercise 6: AutoGen Multi-Agent System

**Objective:** Create a multi-agent system using Microsoft's AutoGen framework.

**Instructions:**

1. Install AutoGen:
   ```bash
   pip install pyautogen
   ```

2. Create a file named `autogen_system.py` with the following structure:

   ```python
   import autogen
   
   # Configure the LLM
   config_list = [
       {
           "model": "gpt-3.5-turbo",
           "api_key": "your-api-key-here"
       }
   ]
   
   # TODO: Create your agents
   
   # TODO: Create a group chat
   
   # TODO: Start the conversation
   ```

3. Complete the code to create a system with at least three agents:
   - An assistant agent
   - A coder agent
   - A user proxy agent

4. Test your system with a programming task: "Create a Python function that calculates the Fibonacci sequence."

5. **Challenge:** Add a critic agent that reviews the code and suggests improvements.

## Exercise 7: Advanced Multi-Agent System

**Objective:** Create a complex multi-agent system that combines multiple frameworks and approaches.

**Instructions:**

1. Design a system that uses both LangGraph for workflow orchestration and CrewAI or AutoGen for agent implementation.

2. Your system should include:
   - At least four different specialized agents
   - A clear workflow with decision points
   - Memory to maintain context across interactions
   - Error handling and fallback mechanisms

3. Implement your system to solve a complex task such as:
   - Researching and writing a comprehensive report on a technical topic
   - Analyzing a dataset and creating visualizations
   - Building and explaining a simple web application

4. **Challenge:** Add a human-in-the-loop component where the system can ask for human input at critical decision points.

## Submission Guidelines

For each exercise:

1. Save your code in a separate Python file with clear comments.
2. Include a brief README explaining:
   - What your code does
   - How to run it
   - Any challenges you encountered
   - How you solved those challenges

3. Be prepared to demonstrate your solution and explain your approach.

## Evaluation Criteria

Your solutions will be evaluated based on:

1. **Functionality:** Does the code work as expected?
2. **Code Quality:** Is the code well-structured, readable, and properly commented?
3. **Creativity:** How innovative is your approach to solving the problem?
4. **Robustness:** How well does your solution handle edge cases and errors?
5. **Understanding:** Can you explain the concepts and techniques used in your solution?

Good luck with the exercises!

