import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dotenv import load_dotenv
load_dotenv()
from nodes.gold_investment_node import gold_investment_api

def main():
    print("Testing Gold Investment Node (personalized, purchase intent detection)\n")
    user_name = input("Please enter your name: ").strip()
    chat_history = []
    print(f"Welcome, {user_name}! Ask anything about gold investment. Type 'exit' to quit.\n")

    while True:
        user_message = input(f"{user_name}: ")
        if user_message.strip().lower() in ["exit", "quit"]:
            break

        result = gold_investment_api(user_message, user_name, chat_history)

        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": result["message"]})

        print("AI:", result["message"])
        if result.get("purchase_triggered"):
            print(">>> Purchase intent detected! Hand off to purchase flow here.\n")
        else:
            print()

if __name__ == "__main__":
    main()
