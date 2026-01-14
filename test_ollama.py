import requests
import json

payload = {
    "model": "llama3",
    "prompt": "Say hello in one sentence",
    "stream": False
}

try:
    print("Testing Ollama API...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Response:\n{data.get('response', '')[:200]}")
    else:
        print(f"Error: {response.text[:300]}")
except Exception as e:
    print(f"Connection Error: {type(e).__name__}: {e}")
