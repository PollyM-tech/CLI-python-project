from datetime import datetime
import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    return phone.isdigit() and len(phone) >= 10

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d") if date_obj else "N/A"

def clear_screen():
    print("\n" * 50)

def exit_program():
    print("\nThank you for using Internet Service Manager. Goodbye!")
    exit()