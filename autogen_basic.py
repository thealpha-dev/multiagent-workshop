import autogen

# Configure the LLM
config_list = [
    {
        "model": "OpenAI.gpt-4.1-mini",
        "api_key": "api-key",
        "base_url": "https://thealpha.dev/api"
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
    message="I need to analyze a dataset of student grades and create a visualization showing the distribution. Can you help me write a Python script for this? Make assumptions as required, the actual dataset is not available, but you can make assumptions that it is available in the root folder where the program will be run",
    llm_config={"config_list": config_list}
)