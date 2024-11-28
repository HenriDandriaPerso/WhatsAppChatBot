# Jonny Sins WhatsApp Chatbot

This Git repository is a proof-of-concept (POC) developed for Goodchat, a company striving to revolutionize chatbot interactions through multiple APIs. The development was completed in 7-8 hours and, as such, there remains considerable scope for improvements and optimizations. The objective was to craft a chatbot representing a public personality that can respond to humans via conventional communication channels. For this POC, WhatsApp was chosen as the communication medium, although Twilio can be easily adapted to respond via SMS as well.

The personality optioned for this project is Jonny Sins. The job listing required some experience with Langgraph, so I developed a basic chatbot leveraging this framework despite having no prior experience with it.

A significant portion of the effort was dedicated to integrating several APIs (Twilio for handling text messages and Heroku for deploying the backend infrastructure). The chatbot backend essentially uses ChatGPT with an enhanced system prompt and employs a straightforward tool for Retrieval-Augmented Generation (RAG) queries utilizing Jonny Sins's biography.

## Testing the Chatbot

To interact with the chatbot, send a message to the number +14155238886 through WhatsApp:
[http://wa.me/14155238886](http://wa.me/14155238886)

Due to the limited subscription tier of Twilio used for this POC, the initial message must be:
```
join gas-aloud
```

Afterwards, feel free to ask any questions.

## Running the Bot Locally

The bot is implemented using FastAPI, with dependencies managed via Poetry.

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```

2. Set up a Python virtual environment:
    ```bash
    python -m venv venv
    ```

3. Install Poetry:
    ```bash
    pip install poetry
    ```

4. Install dependencies:
    ```bash
    poetry install
    ```

5. Define the following environment variables in your system (or load them using a `.env` file):
    - `OPENAI_API_KEY`
    - `TWILIO_ACCOUNT_SID`
    - `TWILIO_AUTH_TOKEN`

6. Run the server using Uvicorn:
    ```bash
    uvicorn main:app
    ```

## Deploying the Server

To ensure Twilio can relay messages to your server, it must be publicly accessible:

- **Option A**: Use Ngrok (note that the server will be dependent on your computer).

- **Option B**: Deploy via Heroku (recommended). The `Procfile` and Python version are predefined; you just need to ensure your Heroku app is set up as a Python application.

## Areas for Improvement

1. **Memory Enhancement**
   - The current use is confined to in-memory storage. This implies conversation history is lost upon server reloads, and multiple workers lack shared memory, potentially causing inconsistencies for users. Utilizing an online database to store conversation history would be beneficial.

2. **Chatbot Interaction Improvements**
   - While ChatGPT is generally reliable, its responses can be stereotypical, lacking the conversational nuances found in human interactions. Finetuning the model on actual informal chats could yield improved realism. Ideally, finetune it on actual chat datasets from Jonny Sins, subject to his approval.

3. **Consideration of Attachments**
   - Twilio facilitates the handling of message attachments. Integrating vision models or text-to-speech capabilities could add significant contextual relevance to the bot's responses.

4. **Tool Enhancements**
   - The addition of advanced features such as voice note generation, contextually relevant GIFs, or real-time event queries related to Jonny Sins would enhance user engagement. Possibilities include sharing direct video links or event alerts. Creativity in augmenting these interactions can make the chatbot invaluable for fans as envisioned by Jonny Sins.

## Conclusion

For inquiries, please reach out to henri.dandria@gmail.com. I look forward to collaborating on similar projects and exploring further advancements in this sphere.