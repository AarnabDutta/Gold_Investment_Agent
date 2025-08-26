import requests
import time
import os

def get_current_gold_price_inr():
    """
    Fetches the current gold price per gram in INR using API Ninjas /commodityprice.
    Reads API URL and key from .env. Returns a consistent dict.
    """
    api_key = os.getenv("GOLDPRICE_API_KEY")
    url = os.getenv("GOLDPRICE_API_URL")

    try:
        if api_key and url:
            response = requests.get(url, headers={"X-Api-Key": api_key}, timeout=10)
            data = response.json()
            # For API Ninjas /commodityprice, price is usually per 10 grams in INR
            if "price" in data:
                price_per_gram = float(data["price"]) / 10  # Adjust if API docs indicate per 10g
                return {
                    "price_per_gram": round(price_per_gram, 2),
                    "currency": "INR",
                    "source": "API Ninjas:commodityprice",
                    "last_updated": time.strftime("%Y-%m-%d %H:%M")
                }
            # If it's a list (other endpoints), also handle:
            elif isinstance(data, list) and len(data) > 0 and "price" in data[0]:
                price_per_gram = float(data[0]["price"]) / 10
                return {
                    "price_per_gram": round(price_per_gram, 2),
                    "currency": "INR",
                    "source": "API Ninjas:commodityprice",
                    "last_updated": time.strftime("%Y-%m-%d %H:%M")
                }
            else:
                print(f"[Warning] Gold price not found in API response: {data}")

    except Exception as e:
        print(f"[Warning] Gold price API error: {e}")

    # Fallback if API fails
    return {
        "price_per_gram": 6500.0,
        "currency": "INR",
        "source": "Static Fallback",
        "last_updated": time.strftime("%Y-%m-%d %H:%M")
    }
