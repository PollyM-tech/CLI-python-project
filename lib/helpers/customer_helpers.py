from models.customer import Customer
from .shared_helpers import validate_email, validate_phone, format_date

def list_customers():
    customers = Customer.get_all()
    if not customers:
        print("\nNo customers found!")
        return
    
    print("\n=== ALL CUSTOMERS ===")
    for idx, customer in enumerate(customers, 1):
        print(f"{idx}. {customer.name} | {customer.email} | {customer.phone}")

def create_customer():
    print("\n=== CREATE NEW CUSTOMER ===")
    router_id = input("Router ID: ").strip()
    name = input("Full Name: ").strip()
    
    while True:
        email = input("Email: ").strip()
        if validate_email(email):
            if not Customer.find_by_email(email):
                break
            print("Email already exists!")
        else:
            print("Invalid email format. Please try again.")
    
    while True:
        phone = input("Phone: ").strip()
        if validate_phone(phone):
            break
        print("Invalid phone number. Please enter at least 10 digits.")
    
    address = input("Address: ").strip()
    
    customer = Customer.create(
        router_id=router_id,
        name=name,
        email=email,
        phone=phone,
        address=address
    )
    
    if customer:
        print(f"\nSuccessfully created customer: {customer.name}")
    else:
        print("\nFailed to create customer.")

def find_customer_by_email():
    email = input("\nEnter customer email: ").strip()
    customer = Customer.find_by_email(email)
    if customer:
        print("\n=== CUSTOMER FOUND ===")
        print(f"Name: {customer.name}")
        print(f"Email: {customer.email}")
        print(f"Phone: {customer.phone}")
        print(f"Address: {customer.address}")
        print(f"Router ID: {customer.router_id}")
    else:
        print("\nCustomer not found!")

def update_customer():
    list_customers()
    try:
        customer_id = int(input("\nEnter customer ID to update: ").strip())
    except ValueError:
        print("Invalid ID format.")
        return
    
    customer = Customer.find_by_id(customer_id)
    if not customer:
        print("Customer not found!")
        return
    
    print("\nLeave blank to keep current value")
    name = input(f"Name [{customer.name}]: ").strip() or customer.name
    
    while True:
        email = input(f"Email [{customer.email}]: ").strip() or customer.email
        if validate_email(email):
            if email == customer.email or not Customer.find_by_email(email):
                break
            print("Email already exists!")
        else:
            print("Invalid email format.")
    
    while True:
        phone = input(f"Phone [{customer.phone}]: ").strip() or customer.phone
        if validate_phone(phone):
            break
        print("Invalid phone number.")
    
    address = input(f"Address [{customer.address}]: ").strip() or customer.address
    
    updated = Customer.update(
        customer_id,
        name=name,
        email=email,
        phone=phone,
        address=address
    )
    
    if updated:
        print("\nCustomer updated successfully!")
    else:
        print("\nFailed to update customer.")

def delete_customer():
    list_customers()
    try:
        customer_id = int(input("\nEnter customer ID to delete: ").strip())
    except ValueError:
        print("Invalid ID format.")
        return
    
    confirm = input(f"Are you sure you want to delete this customer? (y/n): ").lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return
    
    if Customer.delete(customer_id):
        print("Customer deleted successfully!")
    else:
        print("Failed to delete customer.")