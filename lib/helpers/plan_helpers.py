from models.plan import Plan

def list_plans():
    plans = Plan.get_all()
    if not plans:
        print("\n🚫 No plans available.")
        return
    print("\n All Internet Plans:")
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | KES {plan.price} / {plan.duration_months} months")

def create_plan():
    print("\n Create New Plan (type 'q' to cancel)")
    
    name = input("Name: ").strip()
    if name.lower() == 'q': return

    # Check for duplicate
    existing = Plan.find_by_name(name)
    if existing:
        print("❌ A plan with this name already exists.")
        return

    description = input("Description: ").strip()
    if description.lower() == 'q': return

    speed = input("Speed (e.g., 100Mbps): ").strip()
    if speed.lower() == 'q': return

    while True:
        duration_input = input("Duration (months): ").strip()
        if duration_input.lower() == 'q':
            return
        try:
            duration = int(duration_input)
            if duration > 0:
                break
            print("❌ Duration must be a positive number.")
        except ValueError:
            print("❌ Invalid number.")

    while True:
        price_input = input("Price (KES): ").strip()
        if price_input.lower() == 'q':
            return
        try:
            price = float(price_input)
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
    if name.lower() == 'q': return

    plans = Plan.find_by_name(name)
    if not plans:
        print("❌ No plans found.")
        return
    for plan in plans:
        print(f"{plan.id}. {plan.name} | {plan.speed} | KES {plan.price} / {plan.duration_months} months")

def update_plan():
    list_plans()
    try:
        plan_id = int(input("\nEnter Plan ID to update (or 'q' to cancel): ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    plan = Plan.find_by_id(plan_id)
    if not plan:
        print("❌ Plan not found.")
        return

    print(f"\nEditing Plan: {plan.name} (leave blank to keep current values)")

    name = input(f"Name [{plan.name}]: ").strip() or plan.name
    description = input(f"Description [{plan.description or 'None'}]: ").strip() or plan.description
    speed = input(f"Speed [{plan.speed}]: ").strip() or plan.speed

    duration_input = input(f"Duration (months) [{plan.duration_months}]: ").strip()
    price_input = input(f"Price (KES) [{plan.price}]: ").strip()

    try:
        duration = int(duration_input) if duration_input else plan.duration_months
        price = float(price_input) if price_input else plan.price
    except ValueError:
        print("❌ Invalid numeric value.")
        return

    updated = Plan.update(plan_id, name=name, description=description, speed=speed, duration_months=duration, price=price)
    if updated:
        print("✅ Plan updated successfully.")
    else:
        print("❌ Failed to update plan.")

def delete_plan():
    list_plans()
    try:
        plan_id = int(input("\n Enter Plan ID to delete (or 'q' to cancel): ").strip())
    except ValueError:
        print("❌ Invalid ID.")
        return

    confirm = input("⚠️ Are you sure? Type 'yes' to confirm: ").lower()
    if confirm != 'yes':
        print("🚫 Deletion cancelled.")
        return

    if Plan.delete(plan_id):
        print("✅ Plan deleted successfully.")
    else:
        print("❌ Failed to delete plan.")
