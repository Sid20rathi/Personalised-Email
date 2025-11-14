import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import APIRouter , HTTPException , status
from pydantic import BaseModel , HttpUrl
from nodes.nodes import graph

class content_url(BaseModel):
    url : HttpUrl



router1 = APIRouter()


@router1.get("/")
def check_health():
    return{"message": "Email Generation Agnet is working."}


@router1.post("/email")
async def email_generation(content_url:content_url):
    try:
        state =  graph.invoke({'url':content_url.url})

        return {"email_subject":state["email_subject"],"email_body":state["email_body"]}
         

    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error:{e}"
        )
   