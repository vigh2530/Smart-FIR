import subprocess
import shutil
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "mistral")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "120"))

def call_ollama(prompt: str) -> str:
    if shutil.which("ollama") is None:
        return "Ollama Error: Ollama CLI not found."

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=API_TIMEOUT
        )

        if result.returncode != 0:
            return f"Ollama Error: {result.stderr}"

        return result.stdout.strip()

    except Exception as e:
        return f"Ollama Error: {str(e)}"
