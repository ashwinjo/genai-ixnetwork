from phi.agent import Agent
from phi.model.ollama import Ollama
from phi.model.openai import OpenAIChat

from phi.tools.duckduckgo import DuckDuckGo
from ixNetworkRestPyToolkit import IxNetworkRestPy
from ixnetworkdocs_rag import get_knowledge_base
import  manage_topology as mt

from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_result

from dotenv import load_dotenv
import prompts

load_dotenv()
        
knowledge = get_knowledge_base()

# Initialize the IxNetwork Management Agent
ixnetwork_agent = Agent(
    model=Ollama(id="granite3-dense:8b"),
    agent_id="ixnetwork_management",
    name="IxNetwork Management",
    tools=[IxNetworkRestPy()],
    instructions=["Use tables to show data"],
    role="Invokes tools related to IxNetwork Web Session Management like get, create, delete ixnetwork session",
    # show_tool_calls=True, 
    markdown=True,
    add_history_to_messages=True,
    num_history_responses=5,
    # add_datetime_to_instructions=True
)

# Initialize the Web Search Agent
web_agent = Agent(
    name="Web Agent",
    agent_id="websearch_management",
    role="Searches the web for information",
    model=Ollama(id="granite3-dense:8b"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
    add_datetime_to_instructions=True,
)


# Initialize the RAG Agent. Using GPT here for better performance
rag_agent = Agent(
    name="IxNetwork Document Reading RAG Agent",
    model=OpenAIChat(),
    role="Searches IxNetwork Documents for user questions",
    agent_id="documents_management",
    instructions=["Always include sources" , "Use tables to show data"],
    knowledge=knowledge,
    show_tool_calls=True,
    markdown=True,
    search_knowledge=True,
)


# Initialize the SQL Agent to check the port status and ownership details on Ixia Chassiss
# TODO: 


ixia_team = Agent(
    name="Orchestration Agent to delegate tasks to individual agents",
    team=[ixnetwork_agent, web_agent, rag_agent],
    instructions=[
        "First, check if IxNetwork Management Agent can do the job",
        "Second, check if the RAG Agent can get you the answer to your question.",
        "If you still do not have information, then , go to Internet and search for an answer.",
        "Evaluate your response for a confidence score > 0.85"
        "Just return to user whatever tool responds with"
    ],
    read_chat_history=True,
    show_tool_calls=True,
    markdown=True,
    structured_outputs=True,
    debug_mode=True,
    reasoning=True
)


def is_empty_string(value):return value == ''
    
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10), retry=retry_if_result(is_empty_string))
def run_agent_with_retry(agent, query):
    try:
        response = agent.run(message="Question:" + query + " Answer:")
        #import pdb; pdb.set_trace()
        return response.content
    except Exception as e:
        print(f"Error occurred: {e}. Retrying...")
        raise


def main(user_q):
    response = None
    while not response:
        response = run_agent_with_retry(ixia_team, user_q)
        return response
    

