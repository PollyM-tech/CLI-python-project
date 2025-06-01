# lib/helpers/customer_helpers.py

from models.customer import Customer
from .shared_helpers import validate_email, validate_phone

def list_customers():
    customers = Customer.get_all()
    if not customers:
        print("\n🚫 No customers found.")
        return
    print("\n📋 All Customers:")
    for cust in customers:
        print(f"{cust.id}. {cust.name} | {cust.email} | {cust.phone} | {cust.router_id}")

def create_customer():
    print("\n➕ Create Customer")
    router_id = input("Router ID: ").strip()
    name = input("Full Name: ").strip()

    while True:
        email = input("Email: ").strip()
        if not validate_email(email):
            print("❌ Invalid email format.")
        elif Customer.find_by_email(email):
            print("❌ Email already exists.")
        else:
            break

    while True:
        phone = input("Phone: ").strip()
        if validate_phone(phone):
            break
        print("❌ Invalid phone number format.")

    address = input("Address: ").strip()

    customer = Customer.create(router_id, name, email, phone, address)
    if customer:
        print(f"✅ Created: {customer.name}")
    else:
        print("❌ Failed to create customer.")

def find_customer_by_email():
    email = input("\nSearch by email: ").strip()
    customer = Customer.find_by_email(email)
    if customer:
        print(f"\n✅ Found: {customer.name} | {customer.email} | {customer.phone} | {customer.router_id}")
    else:
        print("❌ No customer found.")

def update_customer():
    list_customers()
    try:
        cust_id = int(input("\nEnter Customer ID to update: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    customer = Customer.find_by_id(cust_id)
    if not customer:
        print("❌ Customer not found.")
        return

    name = input(f"Name [{customer.name}]: ").strip() or customer.name

    while True:
        email = input(f"Email [{customer.email}]: ").strip() or customer.email
        if validate_email(email):
            if email == customer.email or not Customer.find_by_email(email):
                break
            print("❌ Email already in use.")
        else:
            print("❌ Invalid email.")

    while True:
        phone = input(f"Phone [{customer.phone}]: ").strip() or customer.phone
        if validate_phone(phone):
            break
        print("❌ Invalid phone number.")

    address = input(f"Address [{customer.address}]: ").strip() or customer.address

    updated = Customer.update(cust_id, name=name, email=email, phone=phone, address=address)
    if updated:
        print("✅ Customer updated.")
    else:
        print("❌ Update failed.")

def delete_customer():
    list_customers()
    try:
        cust_id = int(input("\nEnter Customer ID to delete: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    confirm = input("Are you sure? (y/N): ").lower()
    if confirm != 'y':
        print("🚫 Cancelled.")
        return

    if Customer.delete(cust_id):
        print("✅ Customer deleted.")
    else:
        print("❌ Failed to delete customer.")
