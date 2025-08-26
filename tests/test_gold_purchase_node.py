import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()
from nodes.gold_purchase_node import gold_purchase_node

def main():
    print("Testing Gold Purchase Node with REAL SUPABASE DATABASE! 🚀")
    user_name = input("Please enter your name: ").strip()
    chat_history = []
    pending_purchase = None

    print(f"Welcome, {user_name}! Your purchases will be saved to Supabase!")
    print("Try: 'Buy gold worth 5000 rupees'")
    print("Then provide: '9876543210 your@email.com'")
    print("Type 'exit' to quit.\n")

    while True:
        user_message = input(f"{user_name}: ")
        if user_message.strip().lower() in ["exit", "quit"]:
            break

        result = gold_purchase_node(
            user_message=user_message,
            user_name=user_name,
            db_handle=None,  # Let it auto-create Supabase client
            chat_history=chat_history,
            pending_purchase=pending_purchase
        )

        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": result["message"]})

        print("\nAI:", result["message"], "\n")

        if result.get("success") and result.get("db_updated", False):
            print("🎉 Transaction saved to Supabase! Check your dashboard!")
            pending_purchase = None
        else:
            pending_purchase = result.get("pending_purchase", None)

if __name__ == "__main__":
    main()
