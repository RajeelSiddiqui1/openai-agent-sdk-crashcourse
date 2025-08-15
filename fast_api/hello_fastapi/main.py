from fastapi import FastAPI #type:ignore
from pydantic import BaseModel #type:ignore


class ChatInput(BaseModel):
    message: str

app = FastAPI()

@app.get("/")
def hello_world():
    """
    This is a set test function
    """
    return {'message':'Hello world from Agentic AI'}

@app.post("/chat/start")
def start_chat(input: ChatInput):
    
    print("data recived", input )
    return{"status":"ok"}