import argparse
from faker import Faker
from datetime import datetime, timedelta
import random

from models import create_tables, session
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription

fake = Faker()

# === Argument Parser ===
parser = argparse.ArgumentParser(description="Seed the Internet Service Manager database.")
parser.add_argument('--customers', type=int, default=10, help='Number of customers to seed')
parser.add_argument('--plans', type=int, default=4, help='Number of plans to seed')
parser.add_argument('--subscriptions', type=int, default=10, help='Number of subscriptions to seed')
parser.add_argument('--no-reset', action='store_true', help="Skip resetting tables")
args = parser.parse_args()

# === Optional Reset ===
if not args.no_reset:
    print("⚠️  Resetting database...")
    session.query(Subscription).delete()
    session.query(Customer).delete()
    session.query(Plan).delete()
    session.commit()
    create_tables()
    print("✔ Tables cleared and recreated")
else:
    print("ℹ️  Skipping table reset")

# === Seed Plans ===
print(f"\n📶 Creating {args.plans} internet plans...")
default_plans = [
    {"name": "Basic", "speed": "3 Mbps", "price": 1200, "duration": 1},
    {"name": "Standard", "speed": "5 Mbps", "price": 2500, "duration": 3},
    {"name": "Business", "speed": "10 Mbps", "price": 4000, "duration": 6},
    {"name": "Business Fibre", "speed": "20 Mbps", "price": 7000, "duration": 12},
]

plans_data = default_plans[:args.plans] if args.plans <= len(default_plans) else default_plans

plans = []
for data in plans_data:
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

# === Seed Customers ===
print(f"\n👤 Creating {args.customers} customers...")
customers = []
for _ in range(args.customers):
    customer = Customer.create(
        name=fake.name(),
        email=fake.unique.email(),
        phone=random.choice([
            f"+254{random.randint(700000000, 799999999)}",
            f"07{random.randint(0, 9)}{random.randint(1000000, 9999999)}"
        ]),
        address=fake.address().replace("\n", ", "),
        router_id=f"ROUT{random.randint(1000, 9999)}"
    )
    if customer:
        customers.append(customer)

print(f"✔ Created {len(customers)} customers")

# === Seed Subscriptions ===
print(f"\n📦 Creating {args.subscriptions} subscriptions...")
subscriptions = []
statuses = ["active", "suspended", "expired", "terminated"]

for _ in range(args.subscriptions):
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

print(f"✔ Created {len(subscriptions)} subscriptions")

# === Orphan Check ===
orphans = session.query(Subscription).filter(
    ~Subscription.customer.has(), ~Subscription.plan.has()
).count()

if orphans == 0:
    print("✅ No orphaned subscriptions")
else:
    print(f"⚠️  {orphans} orphaned subscriptions found!")

# === Summary ===
print("\n=== ✅ SEEDING SUMMARY ===")
print(f"Customers: {len(customers)}")
print(f"Plans: {len(plans)}")
print(f"Subscriptions: {len(subscriptions)}")

print("\n=== 👤 SAMPLE CUSTOMERS ===")
for cust in customers[:3]:
    print(f"{cust.name} | {cust.email} | {cust.phone} | Router: {cust.router_id}")

print("\n=== 📶 PLANS ===")
for plan in plans:
    print(f"{plan.name} | {plan.speed} | KSh {plan.price} for {plan.duration_months} months")

print("\n=== 📦 SUBSCRIPTIONS ===")
for sub in subscriptions[:3]:
    print(f"{sub.customer.name} on {sub.plan.name} ({sub.status}) → Ends: {sub.end_date}")

print("\n✅ Database seeding complete!")
