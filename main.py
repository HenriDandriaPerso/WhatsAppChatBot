from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import random
import string
import time

app = FastAPI()

# Simulating a database for conversation history
conversation_history = {}

def generate_message_id():
    return 'msg_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def generate_thread_id():
    return 'thread_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def current_timestamp():
    return int(time.time())

class Message(BaseModel):
    message: str
    thread_id: str

@app.post("/receive-message/")
async def receive_message(message: Message):
    message_id = generate_message_id()
    assistant_id = "asst_abc123"
    run_id = "run_abc123"
    
    response_content = {
        "id": message_id,
        "object": "thread.message",
        "created_at": current_timestamp(),
        "thread_id": message.thread_id,
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": {
                    "value": message.message,
                    "annotations": []
                }
            }
        ],
        "assistant_id": assistant_id,
        "run_id": run_id,
        "attachments": [],
        "metadata": {}
    }
    
    if message.thread_id not in conversation_history:
        conversation_history[message.thread_id] = []

    # Append the new message to the conversation history
    conversation_history[message.thread_id].append(response_content)
    
    return JSONResponse(content=response_content)

@app.post("/receive-file/")
async def receive_file(file: UploadFile = File(...), thread_id: str = Form(...)):
    message_id = generate_message_id()
    assistant_id = "asst_abc123"
    run_id = "run_abc123"

    # Save file to a persistent storage if required
    file_content = await file.read()

    # Simulate storing file content with message (details dependent on file storage mechanisms)
    response_content = {
        "id": message_id,
        "object": "thread.message",
        "created_at": current_timestamp(),
        "thread_id": thread_id,
        "role": "assistant",
        "content": [],
        "assistant_id": assistant_id,
        "run_id": run_id,
        "attachments": [
            {
                "file_name": file.filename,
                "content_type": file.content_type
            }
        ],
        "metadata": {}
    }
    
    if thread_id not in conversation_history:
        conversation_history[thread_id] = []

    # Append the new message to the conversation history
    conversation_history[thread_id].append(response_content)
    
    return JSONResponse(content=response_content)

@app.get("/conversation-history/{thread_id}")
async def get_conversation_history(thread_id: str):
    return conversation_history.get(thread_id, [])

