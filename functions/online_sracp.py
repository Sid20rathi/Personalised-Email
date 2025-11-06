import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from state.state_graph import Graph_state
from langgraph.graph import START,END,StateGraph
from langchain_tavily import TavilySearch, TavilyExtract
import getpass
from langchain.chat_models import init_chat_model
import datetime
from typing import Any, Dict, Optional
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage


load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):

    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")


llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai",temperature=0)



tavily_search_tool = TavilySearch(
    max_results=5,
    topic="general",
)








def online_scrap(state:Graph_state):
    company_name = state["company_name"]


