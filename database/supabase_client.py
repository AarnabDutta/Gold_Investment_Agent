class SupabaseDB:
    def __init__(self):
        import os
        from supabase import create_client, Client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(url, key)

    def write_purchase_record(self, user_name, grams, amount_inr, price_per_gram, phone, email):
        purchase_data = {
            "user_name": user_name,
            "phone": phone,
            "email": email,
            "grams": grams,
            "amount_inr": amount_inr,
            "price_per_gram": price_per_gram
            # purchase_time = defaulted by DB
        }
        result = self.client.table("gold_purchases").insert(purchase_data).execute()
        return result.data is not None

    def get_all_purchases(self):
        """
        Returns all rows from the gold_purchases table (as a list of dicts).
        """
        try:
            result = self.client.table("gold_purchases") \
                .select("*") \
                .order("purchase_time", desc=True) \
                .execute()
            return result.data
        except Exception as e:
            print(f"[DB] Error fetching purchases: {e}")
            return []
