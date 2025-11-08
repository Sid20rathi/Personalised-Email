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
from IPython.display import Image ,display



workflow = StateGraph(Graph_state)

workflow.add_node("data_extraction_from_url",data_from_url)
workflow.add_node("user_data_from_db",get_user_data)
workflow.add_node("email_generation",generate_email)

workflow.add_edge(START,"data_extraction_from_url")
workflow.add_edge("data_extraction_from_url","user_data_from_db")
workflow.add_edge("user_data_from_db","email_generation")
workflow.add_edge("email_generation",END)

graph  = workflow.compile()
start = time.time()

state = graph.invoke({"url":"https://www.linkedin.com/jobs/view/4319116016/?alternateChannel=search&eBP=CwEAAAGaYolb9ILVpa8tmJHmYH-S7jEVtAzv290KCfUCgJ1zHkD3dlLq-25y3ox46LcExEBVRvNkMxgryOvEaEATFmKLpzSxYndymwe7IF1zt0GG_jWtIwOrtvbwhXx6vhfuJ7foVDGIbY0BCESgRxAxG1cFPQIqXtuofwRk9_uwEC-0avJP9OwLNV0u2xN7fmhdKRF7FU6YPQQnz8drtKGbDXEmXxwtnv_xJmOZBTEp1D0756XOCS3I4rI-W8BU2zApJBKhmA5w_NsiLuzhMF4fIHBKHDXX4XgmjgF07jMlfyzeW1UJVZTiXWkRRhrX2oCgUfzNubgzpDn44O7Y3dpL_Tm2nAwuI2yqQjeI4q345mnNiNo1_Ac-Pnw3QBInYyqaE3d2SNDkpF2Q_KmwLpBDMkI4RUg8_n-W2-00C0HINaSAXOTLsmQT7ia8V2mAx1ImkjcDdTUh5V3JS20g7lwjHeItByyVGRsEg9DauVR2Y8baphrlmlQQ-SU&refId=yxuETj5eMQDn7b45RrlpRg%3D%3D&trackingId=uxCNt7ktS2TEygJQ9ltVWw%3D%3D"})

end = time.time()
time_taken = end - start
print("="*50)
print(time_taken)
print("="*50)

print(state["email_subject"])
print("="*50)
print(state["email_body"])