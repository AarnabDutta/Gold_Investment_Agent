
from nodes.gold_investment_node import gold_investment_api
from nodes.gold_purchase_node import gold_purchase_node

class GoldInvestmentSession:
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.chat_history = []
        self.state = "investment"
        self.pending_purchase = None

def run_gold_agent():
    print("🟡 Welcome to the Gold Investment AI Agent!")
    user_name = input("👤 Please enter your name to begin: ").strip()
    print(f"\nHello {user_name}! Ask anything about gold investment, digital gold, or current prices.")
    print("If you want to buy gold, just say so, e.g., 'I want to buy gold.'\n")

    session = GoldInvestmentSession(user_name)

    while True:
        user_message = input(f"{user_name}: ").strip()
        if user_message.lower() in ["quit", "exit"]:
            print("👋 Thank you for using the Gold Investment AI Agent. Stay golden!")
            break

        if session.state == "investment":
            result = gold_investment_api(
                user_message,
                session.user_name,
                chat_history=session.chat_history
            )
            session.chat_history.append({"role": "user", "content": user_message})
            session.chat_history.append({"role": "assistant", "content": result["message"]})

            print("🤖", result["message"])

            if result.get("purchase_triggered"):
                session.state = "purchase"
                session.pending_purchase = None
            continue

        elif session.state == "purchase":
            purchase_result = gold_purchase_node(
                user_message=user_message,
                user_name=session.user_name,
                chat_history=session.chat_history,
                pending_purchase=session.pending_purchase
            )
            print("🤖", purchase_result["message"])
            session.chat_history.append({"role": "user", "content": user_message})
            session.chat_history.append({"role": "assistant", "content": purchase_result["message"]})

            if not purchase_result["success"] and purchase_result.get("pending_purchase"):
                session.pending_purchase = purchase_result["pending_purchase"]
                continue

            if purchase_result["success"]:
                session.state = "investment"
                session.pending_purchase = None
                print("💡 You can type 'exit' to quit or ask about gold again.\n")
            else:
                session.pending_purchase = purchase_result.get("pending_purchase", None)
            continue

        else:
            print("⚠️ Internal state error, resetting conversation.")
            session.state = "investment"
            session.pending_purchase = None

if __name__ == "__main__":
    run_gold_agent()
