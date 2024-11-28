import json
import os
from datetime import datetime
from pathlib import Path
from pprint import pprint

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from langgraph.checkpoint.memory import MemorySaver
from twilio.request_validator import RequestValidator
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from agent.chatbot import compile_chatbot_graph, get_answer_from_chat

graph = compile_chatbot_graph()
memory = MemorySaver()
graph_compiled = graph.compile(checkpointer=memory)


TWILIO_NUMBER = "whatsapp:+14155238886"
DATA_STORAGE = Path("data")
DATA_STORAGE.mkdir(exist_ok=True)
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


# Initialize the Twilio Client
client = Client(account_sid, auth_token)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def validate_twilio_request(request: Request) -> bool:
    validator = RequestValidator(auth_token)
    form_data = await request.form()
    # Absolute URL Twilio used for sending this request
    url = str(request.url)
    # Create a dictionary with all form data from the request
    data = {key: value for key, value in form_data.items()}
    # Retrieve X-TWILIO-SIGNATURE header
    signature = request.headers.get('X-Twilio-Signature', '')
    
    return validator.validate(url, data, signature)

@app.post("/whatsapp/webhook")
async def receive_message(request: Request):
    # Validate the request
    if not await validate_twilio_request(request):
        raise HTTPException(status_code=403, detail="Invalid request signature")
    form_data = await request.form()
    from_number = str(form_data.get('From'))
    body: str = form_data.get('Body') # type: ignore

    if not from_number or not body:
        raise HTTPException(status_code=400, detail="Invalid incoming data")

    # Process the question received from WhatsApp
    response_message = get_answer_from_chat(graph_compiled, 
                            from_number=from_number,
                            to_number_str=TWILIO_NUMBER, message=body)

    # Create response
    twiml = MessagingResponse()
    twiml.message(response_message)

    return PlainTextResponse(str(twiml), media_type="application/xml")

