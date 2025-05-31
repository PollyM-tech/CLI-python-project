from models.subscription import Subscription
from models.customer import Customer
from models.plan import Plan
from datetime import datetime
from .shared_helpers import format_date

def list_subscriptions():
    subs = Subscription.get_all()
    if not subs:
        print("\nNo subscriptions found!")
        return
    
    print("\n=== ALL SUBSCRIPTIONS ===")
    for sub in subs:
        customer = Customer.find_by_id(sub.customer_id)
        plan = Plan.find_by_id(sub.plan_id)
        
        if not customer or not plan:
            print(f"{sub.id}. [Invalid reference - customer or plan not found]")
            continue
            
        status = sub.status.upper()
        print(f"{sub.id}. {customer.name} -> {plan.name} ({status})")
def create_subscription():
    print("\n=== CREATE NEW SUBSCRIPTION ===")
    
    # List customers for selection
    from .customer_helpers import list_customers
    list_customers()
    try:
        customer_id = int(input("\nSelect customer ID: ").strip())
    except ValueError:
        print("Invalid customer ID.")
        return
    
    # List plans for selection
    from .plan_helpers import list_plans
    list_plans()
    try:
        plan_id = int(input("\nSelect plan ID: ").strip())
    except ValueError:
        print("Invalid plan ID.")
        return
    
    customer = Customer.find_by_id(customer_id)
    if not customer:
        print("Customer not found!")
        return
    
    router_id = input(f"Router ID [{customer.router_id}]: ").strip() or customer.router_id
    start_date = datetime.now().date()  # Default to today
    
    subscription = Subscription.create(
        customer_id=customer_id,
        plan_id=plan_id,
        router_id=router_id,
        start_date=start_date
    )
    
    if subscription:
        print("\nSubscription created successfully!")
    else:
        print("\nFailed to create subscription.")

def find_subscriptions_by_customer():
    from .customer_helpers import list_customers
    list_customers()
    try:
        customer_id = int(input("\nEnter customer ID: ").strip())
    except ValueError:
        print("Invalid ID format.")
        return
    
    subs = Subscription.find_by_customer(customer_id)
    if not subs:
        print("\nNo subscriptions found for this customer!")
        return
    
    customer = Customer.find_by_id(customer_id)
    print(f"\n=== SUBSCRIPTIONS FOR {customer.name.upper()} ===")
    for sub in subs:
        plan = Plan.find_by_id(sub.plan_id)
        if not plan:
            print("- [Deleted Plan]")
            continue
            
        print(f"- {plan.name} ({sub.status.upper()})")
        print(f"  Start: {format_date(sub.start_date)}")
        print(f"  End: {format_date(sub.end_date)}")
        print(f"  Router: {sub.router_id}")

def update_subscription_status():
    list_subscriptions()
    try:
        sub_id = int(input("\nEnter subscription ID to update: ").strip())
    except ValueError:
        print("Invalid ID format.")
        return
    
    sub = Subscription.find_by_id(sub_id)
    if not sub:
        print("Subscription not found!")
        return
    
    print("\nCurrent status:", sub.status.upper())
    print("Available statuses: active, paused, cancelled, expired")
    new_status = input("New status: ").strip().lower()
    
    if new_status not in ['active', 'paused', 'cancelled', 'expired']:
        print("Invalid status!")
        return
    
    updated = Subscription.update(sub_id, status=new_status)
    if updated:
        print("\nSubscription status updated successfully!")
    else:
        print("\nFailed to update subscription status.")