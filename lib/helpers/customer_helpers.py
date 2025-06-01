from models.customer import Customer
from .shared_helpers import validate_email, validate_phone

def list_customers():
    customers = Customer.get_all()
    if not customers:
        print("\n🚫 No customers found.")
        return
    print("\n All Customers:")
    for cust in customers:
        print(f"{cust.id}. {cust.name} | {cust.email} | {cust.phone} | Router: {cust.router_id}")

def create_customer():
    print("\n Create Customer (type 'q' to cancel)")
    
    router_id = input("Router ID: ").strip()
    if router_id.lower() == 'q': return

    name = input("Full Name: ").strip()
    if name.lower() == 'q': return

    while True:
        email = input("Email: ").strip()
        if email.lower() == 'q': return
        if not validate_email(email):
            print("❌ Invalid email format.")
        elif Customer.find_by_email(email):
            print("❌ Email already exists.")
        else:
            break

    while True:
        phone = input("Phone: ").strip()
        if phone.lower() == 'q': return
        if validate_phone(phone):
            break
        print("❌ Invalid phone number format.")

    address = input("Address: ").strip()
    if address.lower() == 'q': return

    customer = Customer.create(router_id, name, email, phone, address)
    if customer:
        print(f"✅ Customer created: {customer.name}")
    else:
        print("❌ Failed to create customer.")

def find_customer_by_email():
    email = input("\n Enter email to search: ").strip()
    if email.lower() == 'q': return

    customer = Customer.find_by_email(email)
    if customer:
        print(f"\n✅ Found: {customer.name} | {customer.email} | {customer.phone} | Router: {customer.router_id}")
    else:
        print("❌ No customer found.")

def update_customer():
    list_customers()
    try:
        cust_id = int(input("\n Enter Customer ID to update (or 'q' to cancel): ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    customer = Customer.find_by_id(cust_id)
    if not customer:
        print("❌ Customer not found.")
        return

    print(f"\nEditing customer: {customer.name} (leave blank to keep current value)")

    name = input(f"Name [{customer.name}]: ").strip() or customer.name

    while True:
        email = input(f"Email [{customer.email}]: ").strip() or customer.email
        if validate_email(email):
            existing = Customer.find_by_email(email)
            if email == customer.email or not existing:
                break
            print("❌ Email already in use.")
        else:
            print("❌ Invalid email format.")

    while True:
        phone = input(f"Phone [{customer.phone}]: ").strip() or customer.phone
        if validate_phone(phone):
            break
        print("❌ Invalid phone number.")

    address = input(f"Address [{customer.address}]: ").strip() or customer.address

    updated = Customer.update(cust_id, name=name, email=email, phone=phone, address=address)
    if updated:
        print("✅ Customer updated successfully.")
    else:
        print("❌ Update failed.")

def delete_customer():
    list_customers()
    try:
        cust_id = int(input("\n Enter Customer ID to delete (or 'q' to cancel): ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    confirm = input("⚠️ Are you sure? Type 'yes' to confirm: ").strip().lower()
    if confirm != 'yes':
        print("🚫 Deletion cancelled.")
        return

    if Customer.delete(cust_id):
        print("✅ Customer deleted.")
    else:
        print("❌ Failed to delete customer.")
