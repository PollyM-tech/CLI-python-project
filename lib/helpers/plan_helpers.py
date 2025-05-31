from models.plan import Plan
from .shared_helpers import clear_screen

def list_plans():
    plans = Plan.get_all()
    if not plans:
        print("\nNo plans available!")
        return
    
    print("\n=== INTERNET PLANS ===")
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | ${plan.price}/month")

def create_plan():
    print("\n=== CREATE NEW PLAN ===")
    name = input("Plan Name: ").strip()
    description = input("Description: ").strip()
    
    while True:
        try:
            price = float(input("Monthly Price: ").strip())
            if price > 0:
                break
            print("Price must be positive.")
        except ValueError:
            print("Please enter a valid number.")
    
    speed = input("Speed (e.g., '100 Mbps'): ").strip()
    
    while True:
        try:
            duration = int(input("Duration (months): ").strip())
            if duration > 0:
                break
            print("Duration must be positive.")
        except ValueError:
            print("Please enter a whole number.")
    
    plan = Plan.create(
        name=name,
        description=description,
        price=price,
        speed=speed,
        duration_months=duration
    )
    
    if plan:
        print(f"\nSuccessfully created plan: {plan.name}")
    else:
        print("\nFailed to create plan.")

def find_plan_by_name():
    name = input("\nEnter plan name to search: ").strip()
    plans = Plan.find_by_name(name)
    
    if not plans:
        print("\nNo matching plans found!")
        return
    
    print("\n=== MATCHING PLANS ===")
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | ${plan.price}")

def update_plan():
    list_plans()
    try:
        plan_id = int(input("\nEnter plan ID to update: ").strip())
    except ValueError:
        print("Invalid ID format.")
        return
    
    plan = Plan.find_by_id(plan_id)
    if not plan:
        print("Plan not found!")
        return
    
    print("\nLeave blank to keep current value")
    name = input(f"Name [{plan.name}]: ").strip() or plan.name
    description = input(f"Description [{plan.description}]: ").strip() or plan.description
    
    while True:
        price = input(f"Price [{plan.price}]: ").strip()
        if not price:
            price = plan.price
            break
        try:
            price = float(price)
            if price > 0:
                break
            print("Price must be positive.")
        except ValueError:
            print("Invalid number format.")
    
    speed = input(f"Speed [{plan.speed}]: ").strip() or plan.speed
    
    while True:
        duration = input(f"Duration (months) [{plan.duration_months}]: ").strip()
        if not duration:
            duration = plan.duration_months
            break
        try:
            duration = int(duration)
            if duration > 0:
                break
            print("Duration must be positive.")
        except ValueError:
            print("Invalid number format.")
    
    updated = Plan.update(
        plan_id,
        name=name,
        description=description,
        price=price,
        speed=speed,
        duration_months=duration
    )
    
    if updated:
        print("\nPlan updated successfully!")
    else:
        print("\nFailed to update plan.")

def delete_plan():
    list_plans()
    try:
        plan_id = int(input("\nEnter plan ID to delete: ").strip())
    except ValueError:
        print("Invalid ID format.")
        return
    
    confirm = input(f"Are you sure you want to delete this plan? (y/n): ").lower()
    if confirm != 'y':
        print("Deletion cancelled.")
        return
    
    if Plan.delete(plan_id):
        print("Plan deleted successfully!")
    else:
        print("Failed to delete plan.")