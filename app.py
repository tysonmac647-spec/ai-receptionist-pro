from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import os
import openai
import logging

load_dotenv()

app = FastAPI(title="AI Receptionist Pro")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Store conversation history per call
conversations = {}

SYSTEM_PROMPT = """You are a professional AI receptionist. Be warm, helpful, and concise. 
Your role is to:
1. Greet callers professionally
2. Answer questions about the business
3. Help schedule appointments
4. Take messages
5. Provide information about services and pricing

Keep responses brief (2-3 sentences) and conversational."""

@app.get("/")
async def root():
    return {
        "message": "AI Receptionist Pro API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/voice/incoming")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio calls"""
    form_data = await request.form()
    call_sid = form_data.get('CallSid')
    from_number = form_data.get('From')
    
    logger.info(f"Incoming call from {from_number}, CallSid: {call_sid}")
    
    # Initialize conversation for this call
    conversations[call_sid] = []
    
    response = VoiceResponse()
    response.say(
        "Hello! Thank you for calling AI Receptionist Pro. I'm your AI assistant. How may I help you today?",
        voice="Polly.Amy",
        language="en-GB"
    )
    
    gather = Gather(
        input="speech",
        action="/voice/process",
        method="POST",
        speech_timeout="auto",
        language="en-GB"
    )
    response.append(gather)
    response.redirect("/voice/incoming")
    
    return Response(content=str(response), media_type="application/xml")

@app.post("/voice/process")
async def process_speech(request: Request):
    """Process speech and generate AI response"""
    form_data = await request.form()
    speech_result = form_data.get('SpeechResult')
    call_sid = form_data.get('CallSid')
    
    logger.info(f"Speech from {call_sid}: {speech_result}")
    
    response = VoiceResponse()
    
    if not speech_result:
        response.say("I didn't catch that. Could you please repeat?")
        response.redirect("/voice/incoming")
        return Response(content=str(response), media_type="application/xml")
    
    # Get conversation history
    history = conversations.get(call_sid, [])
    history.append({"role": "user", "content": speech_result})
    
    # Generate AI response using OpenAI
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *history[-10:]  # Keep last 10 messages for context
        ]
        
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        ai_response = completion.choices[0].message.content
        history.append({"role": "assistant", "content": ai_response})
        conversations[call_sid] = history
        
        logger.info(f"AI response: {ai_response}")
        
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        ai_response = "I apologize, I'm having trouble processing that. Could you please repeat your question?"
    
    response.say(ai_response, voice="Polly.Amy", language="en-GB")
    
    # Check if call should end
    end_words = ['goodbye', 'bye', 'thank you', 'thanks', 'that\'s all']
    if any(word in speech_result.lower() for word in end_words):
        response.say("Thank you for calling. Have a wonderful day!")
        response.hangup()
        # Clean up conversation
        if call_sid in conversations:
            del conversations[call_sid]
    else:
        gather = Gather(
            input="speech",
            action="/voice/process",
            method="POST",
            speech_timeout="auto",
            language="en-GB"
        )
        response.append(gather)
    
    return Response(content=str(response), media_type="application/xml")

@app.post("/voice/status")
async def call_status(request: Request):
    """Handle call status updates"""
    form_data = await request.form()
    call_sid = form_data.get('CallSid')
    call_status = form_data.get('CallStatus')
    
    logger.info(f"Call {call_sid} status: {call_status}")
    
    # Clean up when call ends
    if call_status in ['completed', 'busy', 'no-answer', 'failed']:
        if call_sid in conversations:
            del conversations[call_sid]
    
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
