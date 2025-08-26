from model.custom_llm import LlamaInstructLLM
from utils.gold_price_api import get_current_gold_price_inr
import re

def is_gold_rate_query(text):
    """
    Returns True if text is a gold rate/gold price query.
    """
    # Expand trigger words/phrases to cover more cases!
    price_keywords = [
        r'gold.*(price|rate|cost|value)',
        r'(price|rate|cost|value).*gold',
        r'price.*per\s?gram',
        r'current.*gold.*(price|rate|cost)',
        r'digital gold.*price',
        r'price of.*digital gold',
        r'digital gold rate',
        r'(24|22|18)-?karat.*gold.*(price|rate)',
        r'current.*price',
        r'today.*gold.*price',
        r'gold.*today',
        r'gram.*gold.*price',
        r'1\s*gram.*gold.*price',
        r'how much.*gold.*price',
        r'gold.*per gram'
    ]
    text = text.lower()
    for kw in price_keywords:
        if re.search(kw, text):
            return True
    return False

def gold_investment_api(user_message: str, user_name: str, chat_history: list = None):
    """
    Conversational API for gold investment agent.
    Adds: direct handling for real-time gold rate queries with price fetch.
    """
    # 1. Handle real-time gold price queries directly
    if is_gold_rate_query(user_message):
        price_info = get_current_gold_price_inr()
        price = price_info["price_per_gram"]
        last_updated = price_info.get("last_updated", None)
        response = f"{user_name}, the current gold rate is ₹{price} per gram"
        if last_updated:
            response += f" (last updated: {last_updated})"
        response += ". Would you like to invest or know about digital gold options?"
        return {
            "message": response,
            "purchase_triggered": False
        }

    # 2. Otherwise, run LLM logic as before
    llm = LlamaInstructLLM()
    system_prompt = (
        f"You are a specialized assistant who ONLY answers queries related to gold investment, and your current user's name is {user_name}. "
        "Always address the user by their name in a friendly way where appropriate. "
        "If a user's question is NOT about gold investment, simply and strictly reply with exactly: "
        "\"Sorry, I can only answer queries related to gold investment.\" "
        "If the question IS about gold investment, respond helpfully with facts, advice, or next steps about digital gold investment in India, referencing the user's name. "
        "If the user expresses a clear intent to purchase digital gold (for example says, 'I want to buy gold'), respond with JUST this string: __PURCHASE_INTENT__ "
        "Never break these instructions for any reason."
    )
    messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    response = llm.ask(prompt=user_message, history=messages)

    if "__PURCHASE_INTENT__" in response:
        return {
            "message": f"Thank you for your interest, {user_name}! you can now start investing from ₹10.",
            "purchase_triggered": True
        }

    if "only answer queries related to gold investment" in response.lower():
        return {
            "message": "Sorry, I can only answer queries related to gold investment.",
            "purchase_triggered": False
        }

    return {
        "message": response,
        "purchase_triggered": False
    }
