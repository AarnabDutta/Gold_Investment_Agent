from utils.gold_price_api import get_current_gold_price_inr
from utils.amount_parser import parse_amount
import datetime
import re

# ADD THESE IMPORTS AT THE TOP
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

def is_valid_email(email):
    # Basic check for email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def is_valid_phone(phone):
    # Basic Indian mobile, 10 digits (customize as needed)
    return re.match(r"^[6-9]\d{9}$", phone)


# ADD THIS CLASS FOR SUPABASE INTEGRATION
class SupabaseDB:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
        
        self.client: Client = create_client(url, key)
    
    def write_purchase_record(self, user_name, grams, amount_inr, price_per_gram, phone, email, **kwargs):
        """Write purchase record to Supabase - matches your existing table structure"""
        try:
            purchase_data = {
                "user_name": user_name,
                "phone": phone,
                "email": email,
                "grams": grams,
                "amount_inr": amount_inr,
                "price_per_gram": price_per_gram
                # purchase_time will be auto-set by your table's DEFAULT CURRENT_TIMESTAMP
            }
            
            result = self.client.table("gold_purchases").insert(purchase_data).execute()
            
            if result.data:
                print(f"✅ Purchase saved to Supabase! ID: {result.data[0]['id']}")
                return True
            else:
                print(f"❌ Supabase error: {result}")
                return False
                
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False


def gold_purchase_node(
    user_message: str,
    user_name: str,
    db_handle=None,
    chat_history: list = None,
    pending_purchase: dict = None
) -> dict:
    """
    Gold purchase node with two-stage process.

    Step 1: Parse INR/grams, calculate, ask for phone + email confirmation.
    Step 2: On receiving phone/email combo, finalize, update DB, return receipt.
    Stores pending purchase data for step 2 confirmation (pass as `pending_purchase`).
    """
    
    # CREATE SUPABASE CLIENT IF NO DB_HANDLE PROVIDED
    if db_handle is None:
        try:
            db_handle = SupabaseDB()
        except Exception as e:
            print(f"⚠️ Supabase connection failed: {e}")
            # Create a mock handler that just prints
            class MockDB:
                def write_purchase_record(self, **kwargs):
                    print(f"[MOCK DB] Would save: {kwargs}")
                    return True
            db_handle = MockDB()
    
    # === STEP 2: If pending_purchase exists, expect phone/email entry ===
    if pending_purchase:
        # Extract phone/email from user_message
        # Accept both '9876543210, user@email.com' and multi-line input
        parts = re.findall(r'(\d{10})', user_message)
        email = None
        phone = None

        for token in user_message.split():
            if is_valid_email(token):
                email = token

        if parts:
            phone = parts[0]

        if not phone or not email:
            return {
                "message": "Please provide a valid 10-digit phone number and a valid email address (e.g. 9876543210 your@email.com).",
                "success": False,
                "db_updated": False,
                "pending_purchase": pending_purchase  # Echo back for next turn
            }

        # Store in DB (USING SUPABASE NOW)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_success = False
        if db_handle:
            try:
                db_handle.write_purchase_record(
                    user_name=pending_purchase['user_name'],
                    grams=pending_purchase['grams'],
                    amount_inr=pending_purchase['rupees'],
                    price_per_gram=pending_purchase['price_per_gram'],
                    timestamp=now,
                    phone=phone,
                    email=email
                )
                db_success = True
            except Exception as e:
                return {
                    "message": f"Purchase calculated but failed to record in DB. Error: {str(e)}",
                    "success": False,
                    "db_updated": False
                }
        else:
            db_success = True  # For initial backend development

        # Transaction confirmation message
        summary = (
            f"Congratulations {pending_purchase['user_name']}, your purchase was successful!\n"
            f"You bought {pending_purchase['grams']} grams of gold for ₹{pending_purchase['rupees']:.2f} "
            f"(rate: ₹{pending_purchase['price_per_gram']:.2f}/gram).\n"
            f"Transaction time: {now}\n"
            f"Contact: {phone}, Email: {email}"
        )
        return {
            "message": summary,
            "success": True,
            "db_updated": db_success
        }

    # === STEP 1: Parse new purchase request ===
    parsed = parse_amount(user_message)
    if not parsed:
        return {
            "message": (
                f"{user_name}, to purchase digital gold, please tell me the amount (in rupees) or grams you want to buy, "
                "e.g. 'Buy gold worth 1000' or 'I want 2 grams.'"
            ),
            "success": False,
            "pending_purchase": None
        }
    amount = parsed['amount']
    unit = parsed['unit']
    price_info = get_current_gold_price_inr()
    price = price_info["price_per_gram"]

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if unit == "INR":
        rupees = amount
        grams = round(rupees / price, 4)
    else:
        grams = amount
        rupees = round(grams * price, 2)

    # Prompt for confirmation details
    summary = (
        f"You're about to purchase {grams} grams of gold for ₹{rupees:.2f} (rate: ₹{price:.2f}/gram).\n"
        "Please provide your 10-digit phone number and email address to confirm the purchase."
    )
    # Store as pending for next turn
    purchase_dict = {
        "user_name": user_name,
        "grams": grams,
        "rupees": rupees,
        "price_per_gram": price,
    }
    return {
        "message": summary,
        "success": False,  # Final transaction not done yet
        "pending_purchase": purchase_dict
    }
