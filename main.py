from fastapi  import FastAPI 
import os
from route.route import router1
import uvicorn




app = FastAPI()

app.include_router(router1,prefix="/generate",tags=["Email Generation"])



@app.get("/")
def  health_check():
    return{"message":"Email generation agent is live"}



if __name__ =="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)