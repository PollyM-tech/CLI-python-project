import os
import re
from datetime import datetime, date

SUBSCRIPTION_STATUSES = ['active', 'suspended', 'expired', 'terminated']

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^(?:\+254|0)?7\d{8}$'
    return re.match(pattern, phone) is not None


def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d") if date_obj else "N/A"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def exit_program():
    print("\nThank you for using 🌐 PLY Service Manager. Goodbye!")
    exit()

def get_int_input(prompt, min_value=None, allow_blank=False):
    while True:
        user_input = input(prompt).strip()
        if allow_blank and not user_input:
            return None
        try:
            val = int(user_input)
            if min_value is not None and val < min_value:
                print(f"❌ Must be at least {min_value}.")
                continue
            return val
        except ValueError:
            print("❌ Please enter a valid number.")

def get_float_input(prompt, min_value=None):
    while True:
        try:
            val = float(input(prompt).strip())
            if min_value is not None and val < min_value:
                print(f"❌ Must be at least {min_value}.")
                continue
            return val
        except ValueError:
            print("❌ Please enter a valid amount.")

def parse_date_input(prompt, allow_blank=False):
    while True:
        date_input = input(prompt).strip()
        if allow_blank and not date_input:
            return None
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD.")
