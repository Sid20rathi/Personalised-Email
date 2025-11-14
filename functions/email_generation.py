#this file generates the email from he context collected from the user data and url
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


from dotenv import load_dotenv
from state.state_graph import Graph_state
from models.model import Users, ResumeInfo
from config.database import db_session ,engine
from sqlmodel import Session ,select
from pydantic import BaseModel
from langchain.agents import AgentExecutor, create_react_agent
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate




load_dotenv()

class Email_structure(BaseModel):
    email_subject : str
    email_body : str



llm = init_chat_model("google_genai:gemini-2.5-flash", api_key=os.getenv("GOOGLE_API_KEY"),temperature=0)




def generate_email(state:Graph_state):

    try:
       
        extract_prompt =ChatPromptTemplate.from_messages([
        ("system", f'''You the professional email generator. yopu have to generate the email subject and body from the context provided to you and the email should be in the format of a professional email.
        and the email subject should be short and to the point. the body should be under 200-250 words and the email should be like a human has written the email.
         context of the job posting:

         job_description :{state["job_description"]}
         about_company : {state["about_company"]}
         company_name : {state["company_name"]}

         context of the user :
         full_name : {state["full_name"]}
         experience : {state["experience"]}
         skills : {state["skills"]}
         projects : {state["projects"]}


         Importent note : 
         1)Dont include the user name and the company name  in the subject of the email.
         2) if u dont have any information about the user or the job description then u should not include that in the email. and generate a generic email to apply for any job that user can use anytime .
         3) If the user projects matches with the job description then include them in the email .
         4)Dont mention the total duration of experience in the email. (eg - 5 months of experience in total , mention i have experience in the field of web developement and generative Ai)
         5) Dont include  words like "Thank you",etc keep it on point and professional .
         6) If the job description , about the company and company name is not present or not relevant to the user then dont include it in the email.Then generate a generic email using the user info only.
         7) End the email by mentioning , "Regards" , then follow up with the name of the user.
         8) If the user projects and skills matches with the company then mention how the user can be a good candidate for the job.
         9) Include the company name in the email. use dear sir or madam not the hiring team . 
        '''),
        ("human", "Query: {Query}"),
        ])


        chain = extract_prompt | llm.with_structured_output(Email_structure)
        result = chain.invoke({
        "Query": f"Generate an email for the job posting with the context provided to you. the email subject should be short and to the point. the body should be under 200-250 words and the email should be like a human has written the email."
        })

    
        return {
        **state,
        "email_subject": result.email_subject,
        "email_body": result.email_body}
        
    except Exception as e:
        print("Error:",e)


if __name__ =="__main__":
    generate_email(Graph_state)