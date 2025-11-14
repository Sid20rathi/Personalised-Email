import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
import time

from functions.data_extraction_from_url import data_from_url
from functions.email_generation import generate_email
from functions.user_data_from_db import get_user_data
from state.state_graph import Graph_state
from langgraph.graph import StateGraph , START ,END




workflow = StateGraph(Graph_state)

workflow.add_node("data_extraction_from_url",data_from_url)
workflow.add_node("user_data_from_db",get_user_data)
workflow.add_node("email_generation",generate_email)

workflow.add_edge(START,"data_extraction_from_url")
workflow.add_edge("data_extraction_from_url","user_data_from_db")
workflow.add_edge("user_data_from_db","email_generation")
workflow.add_edge("email_generation",END)

graph  = workflow.compile()
