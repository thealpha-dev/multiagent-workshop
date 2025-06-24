# Understanding Multi-Agent Systems
## Workshop Participant Handout

### Workshop Overview

This workshop introduces the concept of Multi-Agent Systems (MAS) in artificial intelligence, focusing on how multiple AI agents can collaborate to solve complex problems. You'll learn about various frameworks for building multi-agent systems, explore real-world applications, and gain hands-on experience creating your own agents.

### Key Concepts

1. **Multi-Agent Systems (MAS)**
   - A computerized system composed of multiple interacting intelligent agents
   - Agents can sense, learn, and act autonomously to achieve goals
   - Enables solving problems beyond the capabilities of single agents

2. **Agent Characteristics**
   - Autonomy: Operates without direct human intervention
   - Social ability: Interacts with other agents and humans
   - Reactivity: Responds to changes in the environment
   - Proactivity: Takes initiative to achieve goals

3. **Agent Architectures**
   - Single Agent: One agent handling all tasks
   - Network: Agents communicating directly with each other
   - Hierarchical: Supervisor agents managing subordinate agents
   - Custom: Specialized architectures for specific applications

### Frameworks Overview

| Framework | Key Features | Best For |
|-----------|-------------|----------|
| **LangChain** | Comprehensive tooling, extensive integrations | General LLM applications, rapid prototyping |
| **LangGraph** | Graph-based orchestration, stateful workflows | Complex workflows, advanced agent coordination |
| **AutoGen** | Conversation-driven collaboration, human-in-the-loop | Dynamic multi-agent conversations, interactive systems |
| **CrewAI** | Role-based collaboration, lightweight | Structured team workflows, role-specific tasks |
| **n8n** | Workflow automation, 400+ integrations | Connecting applications, automating data flow |

### Use Cases

1. **Business**
   - Revenue operations and sales automation
   - Multi-layered customer support
   - Supply chain optimization
   - Strategic planning and decision support

2. **Cybersecurity**
   - Threat detection and response
   - Vulnerability management
   - Intrusion detection systems
   - Security orchestration and automation

3. **Finance**
   - High-frequency and algorithmic trading
   - Fraud detection and risk management
   - Financial compliance automation
   - Personalized financial advice

4. **Software Development**
   - Automated code generation and refactoring
   - Automated testing and debugging
   - Requirements engineering
   - DevOps and deployment automation

5. **Scientific Research**
   - Automated scientific discovery
   - Drug discovery and development
   - Climate modeling and environmental science
   - Data analysis and interpretation

### Environment Setup

```bash
# Create virtual environment
python3 -m venv venv_mas

# Activate on macOS/Linux
source venv_mas/bin/activate

# Activate on Windows
.\venv_mas\Scripts\activate

# Install required packages
pip install langchain langchain_openai wikipedia

pip install crewai

pip install 'crewai[tools]'

pip install autogen
```

### Basic Agent Creation

```python
import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Initialize the LLM
llm = OpenAI(temperature=0)

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
```

### Next Steps in Your Learning Journey

1. **Experiment with Different Frameworks**
   - Try implementing the same agent using different frameworks
   - Compare performance, ease of use, and capabilities

2. **Add More Tools**
   - Integrate additional tools like calculators, web search, or custom APIs
   - Create your own tools for domain-specific tasks

3. **Implement Memory**
   - Add conversation memory to your agents
   - Explore different memory types (buffer, summary, vector)

4. **Build Multi-Agent Systems**
   - Create systems with specialized agents working together
   - Implement different communication patterns between agents

5. **Apply to Real-World Problems**
   - Identify problems in your domain that could benefit from multi-agent systems
   - Start with simple prototypes and gradually increase complexity

### Key Resources

- **Documentation**
  - [LangChain Documentation](https://python.langchain.com/docs/introduction/)
  - [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
  - [AutoGen Documentation](https://microsoft.github.io/autogen/)
  - [CrewAI Documentation](https://docs.crewai.com/introduction)

- **Tutorials**
  - [LangChain: Building an Agent](https://python.langchain.com/docs/tutorials/agents/)
  - [AutoGen Examples](https://microsoft.github.io/autogen/docs/Examples/)
  - [CrewAI: Build Your First Crew](https://docs.crewai.com/guides/crews/first-crew)

- **Communities**
  - [LangChain Discord](https://discord.gg/langchain)
  - [AutoGen GitHub Discussions](https://github.com/microsoft/autogen/discussions)
  - [CrewAI Discord](https://discord.gg/crewai)

### Contact Information

For questions or further discussion after the workshop:

**Presenter:** Mr. Vishnu N C  
**Email:** [Insert email address]  
**LinkedIn:** [Insert LinkedIn profile]  
**GitHub:** [Insert GitHub profile]

### Workshop Feedback

Your feedback is valuable for improving future workshops. Please complete the feedback form provided at the end of the session.

---

© 2025 Understanding Multi-Agent Systems Workshop  
All code examples are provided under the MIT License unless otherwise specified.

