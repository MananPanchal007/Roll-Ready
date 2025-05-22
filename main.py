from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import speech_recognition as sr
import json
import asyncio
import os
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv
import base64
from io import BytesIO
from pydantic import BaseModel
from typing import Dict, List
from interview_analysis import InterviewAnalyzer
from datetime import datetime

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mount static files directory
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Initialize OpenAI client
client = AsyncOpenAI()

# Store active connections and their conversation history
active_connections: Dict[str, WebSocket] = {}
conversation_history: Dict[str, List[Dict]] = {}
user_details_store: Dict[str, Dict] = {}

# Initialize interview analyzer
analyzer = InterviewAnalyzer(openai_api_key=os.getenv("OPENAI_API_KEY"))

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        if client_id not in conversation_history:
            conversation_history[client_id] = []

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.post("/interview")
async def start_interview(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    interviewType: str = Form(...),
    experience: int = Form(...)
):
    client_id = str(len(user_details_store) + 1)
    user_details_store[client_id] = {
        "name": name,
        "email": email,
        "interviewType": interviewType,
        "experience": experience
    }
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user_details": user_details_store[client_id],
            "client_id": client_id
        }
    )

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "text":
                # Store user message
                conversation_history[client_id].append({
                    "role": "user",
                    "content": message_data["content"]
                })
                
                # Send user message back to confirm
                await manager.send_message(
                    json.dumps({
                        "type": "user_message",
                        "content": message_data["content"]
                    }),
                    client_id
                )
                
                # Get AI response
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": message_data["content"]}]
                )
                ai_response = response.choices[0].message.content
                
                # Send AI response
                await manager.send_message(
                    json.dumps({
                        "type": "ai_message",
                        "content": ai_response
                    }),
                    client_id
                )
                
                # Store AI response
                conversation_history[client_id].append({
                    "role": "ai",
                    "content": ai_response
                })
            
            elif message_data["type"] == "finish_interview":
                # Redirect to report page
                return RedirectResponse(url=f"/report/{client_id}")
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)

@app.get("/report/{client_id}")
async def get_report(request: Request, client_id: str):
    if client_id not in conversation_history or client_id not in user_details_store:
        return {"error": "No interview data found"}
    
    # Generate analysis
    analysis = analyzer.analyze_conversation(conversation_history[client_id])
    
    return templates.TemplateResponse(
        "report.html",
        {
            "request": request,
            "user_details": user_details_store[client_id],
            "analysis": analysis,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)