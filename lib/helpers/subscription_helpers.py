from models.subscription import Subscription
from models.customer import Customer
from models.plan import Plan
from .shared_helpers import format_date
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

def list_subscriptions():
    subs = Subscription.get_all()
    if not subs:
        print("\n🚫 No subscriptions found.")
        return
    
    print("\n Subscriptions:")
    for sub in subs:
        print(f"{sub.id}. Customer: {sub.customer.name} | Plan: {sub.plan.name} | Status: {sub.status}")
        print(f"    Start: {format_date(sub.start_date)} → End: {format_date(sub.end_date)}")

def create_subscription():
    print("\nCreate Subscription (type 'q' to cancel)")

    customers = Customer.get_all()
    plans = Plan.get_all()

    if not customers or not plans:
        print("🚫 Ensure both customers and plans exist before creating a subscription.")
        return

    print("\nAvailable Customers:")
    for cust in customers:
        print(f"{cust.id}. {cust.name} ({cust.email})")

    print("\nAvailable Plans:")
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | {plan.price} KES for {plan.duration_months} months")

    cust_input = input("Enter Customer ID: ").strip()
    if cust_input.lower() == 'q':
        return
    plan_input = input("Enter Plan ID: ").strip()
    if plan_input.lower() == 'q':
        return

    try:
        cust_id = int(cust_input)
        plan_id = int(plan_input)
    except ValueError:
        print("❌ Invalid ID format.")
        return

    customer = Customer.find_by_id(cust_id)
    plan = Plan.find_by_id(plan_id)

    if not customer:
        print("❌ Customer not found.")
        return
    if not plan:
        print("❌ Plan not found.")
        return

    start_date = date.today()
    end_date = start_date + relativedelta(months=plan.duration_months)

    subscription = Subscription.create(
        customer_id=customer.id,
        plan_id=plan.id,
        router_id=customer.router_id,
        start_date=start_date,
        end_date=end_date,
        status='active'
    )

    if subscription:
        print(f"✅ Subscription created for {customer.name} ({plan.name}) → Ends: {format_date(end_date)}")
    else:
        print("❌ Failed to create subscription.")

def find_subscriptions_by_customer():
    print("\n🔍 Find Subscriptions by Customer")
    try:
        cust_id = int(input("Enter Customer ID: ").strip())
    except ValueError:
        print("❌ Invalid ID format.")
        return

    customer = Customer.find_by_id(cust_id)
    if not customer:
        print("❌ Customer not found.")
        return

    subs = Subscription.find_by_customer(customer.id)
    if not subs:
        print("No subscriptions found for this customer.")
        return

    print(f"\n📋 Subscriptions for {customer.name}:")
    for sub in subs:
        print(f"- Plan: {sub.plan.name} | Status: {sub.status} | Ends: {format_date(sub.end_date)}")

def update_subscription_status():
    list_subscriptions()
    try:
        sub_id = int(input("\nEnter Subscription ID to update: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    sub = Subscription.find_by_id(sub_id)
    if not sub:
        print("❌ Subscription not found.")
        return

    print("\n📌 New Status Options:")
    print("1. active\n2. suspended\n3. expired\n4. terminated")
    status_map = {'1': 'active', '2': 'suspended', '3': 'expired', '4': 'terminated'}
    choice = input("Choose new status (1-4): ").strip()

    if choice not in status_map:
        print("❌ Invalid choice.")
        return

    new_status = status_map[choice]
    updated = Subscription.update(sub.id, status=new_status)

    if updated:
        print(f"✅ Subscription status updated to '{new_status}'")
    else:
        print("❌ Failed to update status.")

def list_expiring_subscriptions(days=30):
    print("[DEBUG] Called list_expiring_subscriptions()") 
    print(f"\n⏳ Subscriptions expiring in next {days} days:")
    threshold = date.today() + timedelta(days=days)

    subs = Subscription.get_all()
    expiring = [s for s in subs if s.end_date and s.end_date <= threshold]

    if not expiring:
        print("✅ No subscriptions expiring soon.")
        return

    for sub in expiring:
        print(f"{sub.id}. {sub.customer.name} → {sub.plan.name} | Ends: {format_date(sub.end_date)}")

def filter_subscriptions_by_status():
    print("\n🔍 Filter Subscriptions by Status")
    statuses = ['active', 'suspended', 'expired', 'terminated']

    for idx, status in enumerate(statuses, 1):
        print(f"{idx}. {status.capitalize()}")

    choice = input("Choose a status (1-4): ").strip()
    if choice not in ['1', '2', '3', '4']:
        print("❌ Invalid choice.")
        return

    selected_status = statuses[int(choice) - 1]
    subs = Subscription.filter_by_status(selected_status)

    if not subs:
        print(f"🚫 No subscriptions found with status '{selected_status}'.")
        return

    print(f"\n📦 Subscriptions with status '{selected_status}':")
    for sub in subs:
        print(f"- {sub.customer.name} | Plan: {sub.plan.name} | Ends: {format_date(sub.end_date)}")
