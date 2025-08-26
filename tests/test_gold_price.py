import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()
from utils.gold_price_api import get_current_gold_price_inr

def main():
    print("Testing real-time gold price API...\n")
    price_info = get_current_gold_price_inr()
    print("Result:", price_info)
    print(f"Current gold price: ₹{price_info['price_per_gram']} per gram (source: {price_info['source']})")

if __name__ == "__main__":
    main()
