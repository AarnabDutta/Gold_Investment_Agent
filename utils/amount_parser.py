import re

def parse_amount(user_message: str):
    """
    Extracts an investment amount (in INR or grams) from the user's message.
    Returns a dict: {'amount': float, 'unit': 'INR' or 'grams'} or None if not found.
    Supports formats like:
        - "I want to invest 5000 rupees"
        - "Buy gold worth ₹2500"
        - "Purchase 2 grams"
        - "Invest 1000"
        - "Can I buy 0.5 gram?"
        - "Invest one thousand rupees"
    """

    message = user_message.lower()

    # 1. Number in digits (with or without units/rupees/grams)
    matches = re.findall(r'(\d+(?:\.\d+)?)(?:\s*)(rupees?|rs\.?|₹|inr|grams?|g\b)?', message)
    for match in matches:
        num, unit = match
        amount = float(num)
        # Normalize and guess unit
        if unit:
            if 'gram' in unit or 'g' == unit.strip('.'):
                return {"amount": amount, "unit": "grams"}
            else:
                return {"amount": amount, "unit": "INR"}
        else:
            # No explicit unit: assume INR for amounts >= 10, grams for < 10
            return {"amount": amount, "unit": "INR" if amount >= 10 else "grams"}

    # 2. Numbers in words (rudimentary support for English, e.g. "one thousand")
    words_to_numbers = {
        "zero": 0,
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "hundred": 100, "thousand": 1000, "lakh": 100000, "crore": 10000000
    }
    # Trivial logic: look for "X thousand/lakh/crore"
    for key in ["thousand", "lakh", "crore"]:
        pattern = r'(\w+)\s*' + key
        match = re.search(pattern, message)
        if match and match.group(1) in words_to_numbers:
            base = words_to_numbers[match.group(1)]
            total = base * words_to_numbers[key]
            # Guess unit
            if "gram" in message:
                return {"amount": total, "unit": "grams"}
            else:
                return {"amount": total, "unit": "INR"}
    # Example: "one hundred", "two thousand"
    match = re.search(r'(one|two|three|four|five|six|seven|eight|nine|ten)\s*(hundred|thousand|lakh|crore)', message)
    if match:
        n = words_to_numbers[match.group(1)]
        mult = words_to_numbers[match.group(2)]
        amount = n * mult
        if "gram" in message:
            return {"amount": amount, "unit": "grams"}
        else:
            return {"amount": amount, "unit": "INR"}

    return None
