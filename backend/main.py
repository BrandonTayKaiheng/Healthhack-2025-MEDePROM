from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import dbcontext
from uuid import uuid4
from chatbot.llm_bot import Chatbot
from typing import Optional
import os
from dotenv import load_dotenv
from setup.setup_iris import setup

# Load environment variables
load_dotenv()

app = FastAPI()

# Initialize database and chatbot from env vars
username = os.getenv('DB_USERNAME', 'demo')
password = os.getenv('DB_PASSWORD', 'demo')
hostname = os.getenv('DB_HOSTNAME', 'localhost')
port = os.getenv('DB_PORT', '1972')
namespace = os.getenv('DB_NAMESPACE', 'USER')
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Setup IRIS db schema
setup()

# Initialize singletons
db = dbcontext.DbContext(username, password, hostname, port, namespace)
bot = Chatbot(gemini_api_key, db)

# Request models


# Define allowed origins
origins = [
    "http://localhost:5173",  # Allow requests from this origin
    # Add more origins if needed
]

# Add CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class MessageRequest(BaseModel):
    session_id: str
    message: str


class SessionRequest(BaseModel):
    session_id: Optional[str] = None


@app.post("/session")
async def create_session(request: SessionRequest):
    try:
        session_id = request.session_id or str(uuid4())
        session = bot.create_session(session_id)
        initial_message = session.start()
        return {
            "session_id": session_id,
            "message": initial_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/message")
async def send_message(request: MessageRequest):
    try:
        session = bot.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        response = session.send_message(request.message)
        return {
            "session_id": request.session_id,
            "message": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # c = bot.create_chat()
    #
    # while True:
    #     i = input("User: ")
    #
    #     if i == "exit":
    #         break
    #
    #     print(c.send_message(i))
    #
    # print(c)
    # print(c._curated_history)
