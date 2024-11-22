from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from twilio.request_validator import RequestValidator
from fastapi.middleware.cors import CORSMiddleware
from pprint import pprint
from datetime import datetime
from pathlib import Path
import json


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

def add_to_history(from_number: str, data: dict):
    from_number = from_number.replace("+", "")
    from_number = from_number.replace(":", "")
    

    print((str(from_number) + ".json"))
    json_path = DATA_STORAGE / (str(from_number) + ".json")
    if json_path.exists():
        with open(json_path, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(data)
    with open(json_path, "w") as f:
        json.dump(history, f, indent=4)


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
    data = dict(form_data)
    pprint(data)

    print("from_number", from_number)

    add_to_history(str(from_number), data)
        

    

    if not from_number or not body:
        raise HTTPException(status_code=400, detail="Invalid incoming data")

    # Process the question received from WhatsApp
    response_message = process_question(body)

    # Add response to history
    add_to_history(from_number, {"from": "bot", "body": response_message, "timestamp": str(datetime.now())})
    # Create response
    twiml = MessagingResponse()
    twiml.message(response_message)

    return PlainTextResponse(str(twiml), media_type="application/xml")


def process_question(question: str) -> str:
    # Placeholder for question processing logic.
    # This could include querying a database, ML model inference, etc.
    if question.lower() == "hello":
        return "Hi there! How can I help you today?"
    else:
        return "I'm not sure how to answer that yet, but I'm learning! Your question was: " + question
    

def send_message(to_number: str, message: str):
    client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',  # Replace with your Twilio WhatsApp number
        to=to_number
    )
    add_to_history(to_number, {"from": "bot", "body": message, "timestamp": str(datetime.now())})
