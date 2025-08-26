import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.custom_llm import LlamaInstructLLM
from dotenv import load_dotenv

def main():
    load_dotenv()
    print("Testing Meta Llama 3.3 8B Instruct (OpenRouter wrapper)")
    llm = LlamaInstructLLM()
    while True:
        prompt = input("\nUser: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        response = llm.ask(prompt)
        print("AI:", response)

if __name__ == "__main__":
    main()
