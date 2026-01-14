import subprocess
import shutil

MODEL_NAME = "llama3"

def call_ollama(prompt: str) -> str:
    if shutil.which("ollama") is None:
        return "Ollama Error: Ollama CLI not found."

    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            timeout=180
        )

        if result.returncode != 0:
            return f"Ollama Error: {result.stderr}"

        return result.stdout.strip()

    except Exception as e:
        return f"Ollama Error: {str(e)}"
