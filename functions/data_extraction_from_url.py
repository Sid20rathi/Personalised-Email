import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from state.state_graph import Graph_state
from pydantic import BaseModel, Field 
import google.genai as genai
from google.genai.types import Tool, GenerateContentConfig


load_dotenv()

class JobDetails(BaseModel):
    """Structured data extracted from the job posting summary."""
    job_description: str = Field(description="The detailed description of the job role and responsibilities.")
    about_company: str = Field(description="The general information about the company.")
    company_name: str = Field(description="The name of the company posting the job.")

client = genai.Client()
model_id = "gemini-2.5-flash"
tools = [
  {"url_context": {}},
]


llm = init_chat_model("google_genai:gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
prompt = hub.pull("hwchase17/react")

parser_prompt = hub.pull("hwchase17/react")



def data_from_url(state: Graph_state):
   



    url =state["url"] 
    
   

    try:
      
       
        response = client.models.generate_content(
            model=model_id,
            contents=f'''from the provided url {url},please provide me the  job_description ,about_company ,company_name in detail.
            if there is no job description available then please provide me the about_company and company_name in detail.and if company name , about company and job description are not available then return None for the missing fields''',
            config=GenerateContentConfig(
                tools=tools,
            )
        )

        agent_output = response.text
 


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
    data_from_url(Graph_state())






    
