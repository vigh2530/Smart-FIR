from ollama.ollama_client import call_ollama

test_prompt = "Say hello in one sentence."

print("Testing Ollama with mistral model...")
try:
    response = call_ollama(test_prompt)
    print(f"✅ Success!\nResponse: {response[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")
