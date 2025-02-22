# llm_adapter.py
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --------------------------
# OpenAI Integration Example
# --------------------------
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(message: str) -> str:
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # or another supported model
        messages=[{"role": "user", "content": message}],
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"OpenAI error: {str(e)}"

# --------------------------
# Claude Integration Example
# --------------------------
# You might need to install the anthropic package:
# pip install anthropic
# (Check Anthropic's docs for details and adjust as needed.)
try:
    from anthropic import AnthropicClient
except ImportError:
    AnthropicClient = None

def get_claude_response(message: str) -> str:
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not AnthropicClient:
        return "Anthropic client not installed."
    client = AnthropicClient(api_key=claude_api_key)
    try:
        # Note: Adjust the parameters based on the actual API spec.
        response = client.completion(
            prompt=f"User: {message}\nAssistant:",
            model="claude-v1",  # Example model name
            max_tokens_to_sample=150,
            temperature=0.7,
        )
        return response.get("completion", "").strip()
    except Exception as e:
        return f"Claude error: {str(e)}"

# --------------------------
# Grok Integration (Placeholder)
# --------------------------
import requests

def get_grok_response(message: str) -> str:
    # Replace with the actual endpoint and parameters per Grok's API documentation.
    try:
        # Example using requests (adjust URL and payload as needed)
        url = "https://api.grok.example.com/chat"  # Placeholder URL
        headers = {"Authorization": f"Bearer {os.getenv('GROK_API_KEY', '')}"}
        payload = {"message": message}
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data.get("reply", f"Grok reply for: {message}")
    except Exception as e:
        return f"Grok error: {str(e)}"

# --------------------------
# Gemini Integration (Placeholder)
# --------------------------
def get_gemini_response(message: str) -> str:
    # Replace with the actual Gemini API integration details.
    return f"Gemini simulated response for: {message}"

# --------------------------
# Local LLM Integration Example
# --------------------------
# We can use Hugging Face Transformers for a local model.
# Install with: pip install transformers torch
from transformers import pipeline

# Initialize the pipeline globally (this loads the model only once).
try:
    local_pipeline = pipeline("text-generation", model="gpt2")
except Exception as e:
    local_pipeline = None

def get_local_response(message: str) -> str:
    if not local_pipeline:
        return "Local model not available."
    try:
        results = local_pipeline(message, max_length=50)
        return results[0]["generated_text"]
    except Exception as e:
        return f"Local LLM error: {str(e)}"

# --------------------------
# Unified API Function
# --------------------------
def get_llm_response(model: str, message: str) -> str:
    """
    Routes the message to the appropriate LLM integration.
    Defaults to 'local' if model is unrecognized.
    """
    model = model.lower()
    if model == "openai":
        return get_openai_response(message)
    elif model == "grok":
        return get_grok_response(message)
    elif model == "claude":
        return get_claude_response(message)
    elif model == "gemini":
        return get_gemini_response(message)
    elif model == "local":
        return get_local_response(message)
    else:
        return f"Unrecognized model '{model}'. Using local LLM: {get_local_response(message)}"
