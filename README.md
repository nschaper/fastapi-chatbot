# FastAPI Chatbot with Multiple LLM Integrations

A simple FastAPI-based chatbot that can route messages to multiple Large Language Models (LLMs), including OpenAI, Claude, Grok, Gemini, and local models (via Hugging Face Transformers). Includes a web-based chat interface using HTML/JavaScript.

## Features

- **FastAPI** backend providing REST and WebSocket endpoints  
- **Local & Cloud LLM Support** via a unified adapter (`llm_adapter.py`)  
- **Simple Frontend** served by FastAPI’s static files  
- **Optional WebSockets** for real-time chat  
- **Docker Support** for easy deployment  
- **.env** configuration for sensitive credentials  

---

## Getting Started

### 1. Clone the Repository

    git clone https://github.com/your-username/your-fastapi-chatbot.git
    cd your-fastapi-chatbot

### 2. Create and Activate a Virtual Environment

**macOS/Linux (using `python3` and `venv`):**

    python3 -m venv venv
    source venv/bin/activate

**Windows (using Command Prompt):**

    python -m venv venv
    venv\Scripts\activate

### 3. Install Dependencies

    pip install --upgrade pip
    pip install -r requirements.txt

### 4. Create a `.env` File

In the project root, create a file named `.env` and add your environment variables. For example:

    # .env
    OPENAI_API_KEY=your-openai-api-key
    CLAUDE_API_KEY=your-claude-api-key
    GROK_API_KEY=your-grok-api-key
    # etc.

Be sure to keep this file out of source control to protect your keys (the project’s `.gitignore` should already ignore it).

### 5. Run the App Locally

    uvicorn main:app --reload

- Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000) to view the chat interface.  
- Test the `/ping` endpoint at [http://127.0.0.1:8000/ping](http://127.0.0.1:8000/ping).  

---

## Docker Instructions

### 1. Build the Docker Image

    docker build -t my-chatbot:latest .

### 2. Run the Container

    docker run -p 8000:8000 --env-file .env my-chatbot:latest

Your app will be accessible at [http://localhost:8000](http://localhost:8000).

**Optional**: If you have multiple services or prefer easier orchestration, consider adding a `docker-compose.yml` and running:

    docker-compose up --build

---

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this software dedicate any and all copyright interest in the software to the public domain. We make this dedication for the benefit of the public at large and to the detriment of our heirs and successors. We intend this dedication to be an overt act of relinquishment in perpetuity of all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to [The Unlicense](https://unlicense.org).
