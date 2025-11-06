import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from state.state_graph import Graph_state
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from state.state_graph import Graph_state
from pydantic import BaseModel, Field 


load_dotenv()

class JobDetails(BaseModel):
    """Structured data extracted from the job posting summary."""
    job_description: str = Field(description="The detailed description of the job role and responsibilities.")
    about_company: str = Field(description="The general information about the company.")
    company_name: str = Field(description="The name of the company posting the job.")

sync_browser = create_sync_playwright_browser()
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=sync_browser)
tools = toolkit.get_tools()

llm = init_chat_model("google_genai:gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
prompt = hub.pull("hwchase17/react")

parser_prompt = hub.pull("hwchase17/react")



def playwrigtht(state: Graph_state):

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        handle_parsing_errors=True,
        max_iteratons=10
    )

    url ="https://www.linkedin.com/jobs/view/4309474739/?alternateChannel=search&eBP=CwEAAAGaSr7CpTjHmQW9TvSiD8PEyjuaRxC-piQ9-wjgUQhvYhF811YU14PYjLIjUTHrcJxJe9Bv8U2osALsp7QgmXvWEmKF_KrlYsickg653IBMACBCSMtH0QneoNnl7jI1ijwp7Ls1qoG8OoyjqzJUbNRDICmSzIW7JIrZMNikMW4vO8_xdabTMwKM8uy7rSg31NH6PDrQXIBk592vcAbPzBQhUZ6ZnT7G3xx16eXHO2XQjEoxRY4zTx67kHPW8cxkvP_SV2a_olqRyJUs6Ui9op87PnfgtCmqAmJSTfbr_whkHX5sUfQ0IYrw5xNxVOc6l-tFl8RWheIrb0O20KwpCk-cL3w17hDTxfeNDtUjAyaWG0XaduG1Kr-q6QVvXO4Dx_8M54lsitGrwkTBSEjuwHN3pUBOKBPO6cKRI6w_O0F-zmffrRM5Or5mUATQ9uh1J2rHdlTBYGlAby3HVwQXWWhb4Um6LCd-GR2f1o0rSfgouQjj4MhQSHkednCd&refId=niFdWhD5%2B0uOPbBQboiFbg%3D%3D&trackingId=MizqNK9ON9%2FWTcE1nLdtAA%3D%3D" 
    command = {
        "input": f"Go to {url} and give me the job description in detail and about the company and provide contact info of the person posted the job"
    }

    try:
      
        result = agent_executor.invoke(command)
        agent_output = result["output"]


        parser_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a data extraction bot. Extract the required fields from the following text."),
            ("human", "Text to parse: {text}"),
        ])

        
        structured_parser = parser_prompt | llm.with_structured_output(JobDetails)
        parsed_data = structured_parser.invoke({"text": agent_output})
        
     
        return {
            **state,
            "job_description": parsed_data.job_description,
            "about_company": parsed_data.about_company,
            "company_name": parsed_data.company_name,
        }

    except Exception as e:
        print("Error:",e)
    





if __name__ == "__main__":
    playwrigtht(Graph_state)






    
