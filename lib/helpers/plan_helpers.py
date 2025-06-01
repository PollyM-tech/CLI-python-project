# lib/helpers/plan_helpers.py

from models.plan import Plan

def list_plans():
    plans = Plan.get_all()
    if not plans:
        print("\n🚫 No plans available.")
        return
    print("\n📶 All Internet Plans:")
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | KES {plan.price} / {plan.duration_months} months")

def create_plan():
    print("\n➕ Create New Plan")
    name = input("Name: ").strip()
    description = input("Description: ").strip()
    speed = input("Speed (e.g., 100Mbps): ").strip()
    duration = int(input("Duration (months): ").strip())

    while True:
        try:
            price = float(input("Price (KES): ").strip())
            if price > 0:
                break
            print("❌ Price must be positive.")
        except ValueError:
            print("❌ Invalid price.")

    plan = Plan.create(name, description, price, speed, duration)
    if plan:
        print(f"✅ Plan created: {plan.name}")
    else:
        print("❌ Failed to create plan.")

def find_plan_by_name():
    name = input("Search plan by name: ").strip()
    plans = Plan.find_by_name(name)
    if not plans:
        print("❌ No plans found.")
        return
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | KES {plan.price}")

def update_plan():
    list_plans()
    try:
        plan_id = int(input("\nEnter Plan ID: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    plan = Plan.find_by_id(plan_id)
    if not plan:
        print("❌ Plan not found.")
        return

    name = input(f"Name [{plan.name}]: ").strip() or plan.name
    description = input(f"Description [{plan.description}]: ").strip() or plan.description
    speed = input(f"Speed [{plan.speed}]: ").strip() or plan.speed
    duration = input(f"Duration [{plan.duration_months}]: ").strip()
    price = input(f"Price [{plan.price}]: ").strip()

    try:
        duration = int(duration) if duration else plan.duration_months
        price = float(price) if price else plan.price
    except ValueError:
        print("❌ Invalid input.")
        return

    updated = Plan.update(plan_id, name=name, description=description, speed=speed, duration_months=duration, price=price)
    if updated:
        print("✅ Plan updated.")
    else:
        print("❌ Update failed.")

def delete_plan():
    list_plans()
    try:
        plan_id = int(input("\nEnter Plan ID to delete: ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    confirm = input("Are you sure? (y/N): ").lower()
    if confirm != 'y':
        print("🚫 Cancelled.")
        return

    if Plan.delete(plan_id):
        print("✅ Plan deleted.")
    else:
        print("❌ Failed to delete.")
