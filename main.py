from dotenv import load_dotenv
import os

# Load environment variables from .env first
load_dotenv()

from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llm_adapter import get_llm_response, get_openai_response

app = FastAPI()

# Optional: If you still have a REST-based /chat endpoint, keep it here.
# class ChatMessage(BaseModel):
#     message: str
#     model: str = "openai"
#
# @app.post("/chat")
# async def chat_post(chat_msg: ChatMessage):
#     # Non-streaming fallback example
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": chat_msg.message}],
#         temperature=0.7,
#     )
#     reply = completion.choices[0].message.content
#     return {"reply": reply}

@app.get("/ping")
async def ping():
    return {"message": "pong"}

# If you serve static files, do it here
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket route for real-time, token-by-token streaming from OpenAI.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            user_message = data.get("message", "")
            model_name = data.get("model", "openai")

            async for token in get_openai_response(user_message):
                await websocket.send_json({
                    "type": "token",
                    "content": token
                })
            
            # Send an "end" message to signal completion
            await websocket.send_json({
                "type": "end"
            })

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Error in WebSocket: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "content": str(e)
            })
        except:
            print("Could not send error message to client")
