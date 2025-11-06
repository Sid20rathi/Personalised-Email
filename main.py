import os
from dotenv import load_dotenv
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

tavily_extract_tool = TavilyExtract()

tools=[tavily_search_tool,tavily_extract_tool]

today = datetime.datetime.today().strftime("%D")



prompt = """You are a helpful reaserch assistant, you will be given a query and you will need to
    search the web for the most relevant information then extract content to gain more insights. The date today is {today}."""
# Create an agent that can use tools
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)



user_input =  "provide me the email id to apply for job in apple india"


response = agent.invoke({"messages": [HumanMessage(content=user_input)]})

print(response)









