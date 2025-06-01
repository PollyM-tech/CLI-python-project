from faker import Faker
from datetime import datetime, timedelta
import random
from models import create_tables, session
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription

fake = Faker()
print("Seeding database...")

# Reset database
session.query(Subscription).delete()
session.query(Customer).delete()
session.query(Plan).delete()
session.commit()
create_tables()
print("✔ Cleared and recreated database tables")

# Plans
plans_info = [
    {"name": "Basic", "speed": "3 Mbps", "price": 1200, "duration": 1},
    {"name": "Standard", "speed": "5 Mbps", "price": 2500, "duration": 3},
    {"name": "Business", "speed": "10 Mbps", "price": 4000, "duration": 6},
    {"name": "Business Fibre", "speed": "20 Mbps", "price": 7000, "duration": 12},
]

plans = []
for data in plans_info:
    plan = Plan.create(
        name=data["name"],
        speed=data["speed"],
        price=data["price"],
        duration_months=data["duration"],
        description=fake.sentence(nb_words=6)
    )
    if plan:
        plans.append(plan)
print(f"✔ Created {len(plans)} plans")

# Customers
customers = []
for _ in range(12):
    customer = Customer.create(
        name=fake.name(),
        email=fake.unique.email(),
        phone=f"+254{random.randint(700000000, 799999999)}",
        address=fake.address().replace("\n", ", "),
        router_id=f"ROUT{random.randint(1000, 9999)}"
    )
    if customer:
        print(f"✔ Created customer: {customer.name}")
        customers.append(customer)

# Subscriptions
subscriptions = []
statuses = ["active", "suspended", "expired"]
for _ in range(10):
    cust = random.choice(customers)
    plan = random.choice(plans)
    start = fake.date_between(start_date="-6M", end_date="today")
    end = start + timedelta(days=plan.duration_months * 30)
    sub = Subscription.create(
        customer_id=cust.id,
        plan_id=plan.id,
        router_id=cust.router_id,
        start_date=start,
        end_date=end,
        status=random.choice(statuses)
    )
    if sub:
        subscriptions.append(sub)

print(f"✔ Created {len(customers)} customers")
print(f"✔ Created {len(subscriptions)} subscriptions")

# Validation
print("Running validation checks...")
orphans = session.query(Subscription).filter(
    ~Subscription.customer.has(), ~Subscription.plan.has()
).count()

print(f"Customers: {len(customers)} | Plans: {len(plans)} | Subscriptions: {len(subscriptions)}")
if orphans == 0:
    print("✔ No orphaned subscriptions found")
else:
    print(f"⚠️  Found {orphans} orphaned subscriptions!")

# Display Summary
print("\n=== CUSTOMERS ===")
for cust in customers[:5]:
    print(f"ID: {cust.id}, Name: {cust.name}, Email: {cust.email}, Router: {cust.router_id}, Phone: {cust.phone}")

print("\n=== INTERNET PLANS ===")
for plan in plans:
    print(f"ID: {plan.id}, Name: {plan.name}, Speed: {plan.speed}, KSh {plan.price:.2f}, Duration: {plan.duration_months} mo")

print("\n=== SUBSCRIPTIONS ===")
for sub in subscriptions[:5]:
    print(f"Sub ID: {sub.id}, Customer: {sub.customer.name}, Plan: {sub.plan.name}, Status: {sub.status}, Start: {sub.start_date}, End: {sub.end_date}")

print("\n✅ Database seeded successfully!")
