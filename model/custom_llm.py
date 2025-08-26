import requests
import os
import json

class LlamaInstructLLM:
    def __init__(self):
        self.api_url = os.getenv("OPENROUTER_API_URL")
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.model = os.getenv("LLAMA_MODEL_ID")

        missing = []
        if not self.api_url:
            missing.append('OPENROUTER_API_URL')
        if not self.api_key:
            missing.append('OPENROUTER_API_KEY')
        if not self.model:
            missing.append('LLAMA_MODEL_ID')
        if missing:
            raise ValueError(f"Missing required .env variables: {', '.join(missing)}")

    def ask(self, prompt, history=None, temperature=0.2, max_tokens=1024):
        messages = history[:] if history else []
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        response = requests.post(self.api_url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        data = response.json()

        return data['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    llm = LlamaInstructLLM()
    reply = llm.ask("Is this Llama wrapper working?")
    print(reply)
