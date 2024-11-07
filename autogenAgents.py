# it is to be run in google colab

!pip install git+https://github.com/microsoft/autogen.git@v0.2.25
!pip install dask[dataframe]
!pip install --upgrade google-generativeai
# Import necessary libraries
import os
from autogen import AssistantAgent, UserProxyAgent
from google.colab import userdata

# Set your API key directly in the code (replace with your actual API key)
api_key = "your api key of gemini"

# Define the maximum number of user replies
MAX_USER_REPLIES = 5

# Define the starting message for the chat
INPUT_START_MESSAGE = """
write java program to interact with kafka cluster
"""

# Define your model configuration
config_list_gemini = [
    {
        "model": "gemini-1.5-pro-latest",
        "api_key": api_key,
        "api_type": "google"
    }
]

# Initialize the assistant agent with the Gemini model configuration
assistant = AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 41,
        "config_list": config_list_gemini,
        "seed": 42
    },
)

# Initialize the user proxy agent
try:
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=MAX_USER_REPLIES,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False
        },
    )
except Exception as e:
    print(f"The following error happened: {str(e)}")
    exit()

# Start the chat between the user proxy and the assistant agent
chat_response = user_proxy.initiate_chat(
    assistant,
    message=INPUT_START_MESSAGE,
)

# Accessing chat_id and chat_history safely
chat_id = getattr(chat_response, 'chat_id', None)
chat_history = getattr(chat_response, 'chat_history', [])
cost_info = getattr(chat_response, 'cost', {})

# Display chat ID
if chat_id:
    print(f"CHAT REF: {chat_id}")
else:
    print("Chat ID is not available.")

# Access and print cost details safely
if isinstance(cost_info, dict):
    total_cost = cost_info.get(1, "Cost data not available") 
    # Adjust based on actual structure
    print(f"COST OF TRANSACTION: {total_cost}")
else:
    print("Cost data format unexpected:", cost_info)

# Display conversation content
for conv in chat_history:
    content = conv.get('content', "")
    active_role = conv.get('role', "")
    print(f"{active_role}: {content}")

print("program executed")
