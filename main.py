from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llm_adapter import get_llm_response

app = FastAPI()

class ChatMessage(BaseModel):
    message: str
    model: str = "local"  # Default model if none is specified

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/chat")
async def chat_post(chat_msg: ChatMessage):
    # Route the message to the appropriate LLM stub
    reply = get_llm_response(chat_msg.model, chat_msg.message)
    return {"reply": reply}

# Mount static files at '/static'
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the homepage at '/'
@app.get("/")
async def index():
    return FileResponse("static/index.html")

# WebSocket endpoint
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()  
            # data should be a dict like {"message": "...", "model": "..."}
            user_message = data.get("message", "")
            model = data.get("model", "local")
            
            # Generate reply using your LLM adapter
            reply = get_llm_response(model, user_message)
            
            # Send reply back to client
            await websocket.send_json({"reply": reply})
    except WebSocketDisconnect:
        print("Client disconnected.")