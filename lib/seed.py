#!/usr/bin/env python3

from faker import Faker
from random import choice, randint
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from models import Session
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription
import re

# ========== Setup ==========
fake = Faker()
session = Session()

# Validation patterns
EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
PHONE_REGEX = r'^\d{10,15}$'
ROUTER_ID_REGEX = r'^ROUT\d{6}$'

# ========== Validators ==========
def validate_email(email):
    return re.match(EMAIL_REGEX, email) is not None

def validate_phone(phone):
    return re.match(PHONE_REGEX, phone) is not None

def validate_router_id(router_id):
    return re.match(ROUTER_ID_REGEX, router_id) is not None

def generate_valid_phone():
    while True:
        phone = fake.numerify(text='##########')
        if validate_phone(phone):
            return phone

def generate_valid_router_id():
    return f"ROUT{fake.unique.random_number(digits=6)}"

# ========== Data Creation Functions ==========
def clear_existing_data():
    """Clear all existing data with proper error handling"""
    try:
        session.query(Subscription).delete()
        session.query(Customer).delete()
        session.query(Plan).delete()
        session.commit()
        print("✔ Cleared existing data")
    except Exception as e:
        session.rollback()
        print(f"❌ Error clearing data: {e}")
        raise

def create_plans():
    """Create validated internet plans"""
    plans_data = [
        {"name": "Basic", "description": "Entry-level internet", "price": 29.99, "speed": "50 Mbps", "duration": 12},
        {"name": "Standard", "description": "Family internet", "price": 49.99, "speed": "100 Mbps", "duration": 12},
        {"name": "Premium", "description": "High-speed internet", "price": 79.99, "speed": "200 Mbps", "duration": 12},
        {"name": "Ultra", "description": "Fiber optic", "price": 99.99, "speed": "1 Gbps", "duration": 24}
    ]

    plans = []
    for data in plans_data:
        try:
            if data["price"] <= 0 or data["duration"] <= 0:
                raise ValueError("Price and duration must be positive")

            plan = Plan.create(
                name=data["name"],
                description=data["description"],
                price=data["price"],
                speed=data["speed"],
                duration_months=data["duration"]
            )
            plans.append(plan)
        except Exception as e:
            print(f"❌ Error creating plan {data['name']}: {e}")
            continue

    try:
        session.commit()
        print(f"✔ Created {len(plans)} internet plans")
        return plans
    except IntegrityError:
        session.rollback()
        print("❌ Duplicate plan detected")
        return []
    except Exception as e:
        session.rollback()
        print(f"❌ Error committing plans: {e}")
        return []

def create_customers(count=20):
    """Generate validated customers"""
    customers = []
    attempts = 0
    max_attempts = count * 2

    while len(customers) < count and attempts < max_attempts:
        attempts += 1
        try:
            router_id = generate_valid_router_id()
            email = fake.unique.email()
            phone = generate_valid_phone()

            if not (validate_email(email) and validate_phone(phone) and validate_router_id(router_id)):
                raise ValueError("Validation failed")

            customer = Customer.create(
                router_id=router_id,
                name=fake.name(),
                email=email,
                phone=phone,
                address=fake.address().replace('\n', ', ')[:100]
            )
            customers.append(customer)
        except IntegrityError:
            session.rollback()
            continue
        except Exception as e:
            session.rollback()
            print(f"⚠️ Skipping customer: {e}")
            continue

    try:
        session.commit()
        print(f"✔ Created {len(customers)} validated customers")
        return customers
    except Exception as e:
        session.rollback()
        print(f"❌ Error committing customers: {e}")
        return []

def create_subscriptions(customers, plans, count=30):
    """Create validated subscriptions"""
    if not customers or not plans:
        print("❌ No customers or plans available for subscriptions")
        return

    status_choices = ['active'] * 7 + ['paused'] * 2 + ['cancelled']

    created = 0
    for _ in range(count):
        try:
            customer = choice(customers)
            plan = choice(plans)
            status = choice(status_choices)

            start_date = fake.date_between(start_date='-2y', end_date='today')
            end_date = None

            if status in ['paused', 'cancelled']:
                end_date = fake.date_between(start_date=start_date, end_date='today')

            if end_date and end_date < start_date:
                end_date = start_date + timedelta(days=1)

            Subscription.create(
                customer_id=customer.id,
                plan_id=plan.id,
                router_id=customer.router_id,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            created += 1
        except IntegrityError:
            session.rollback()
            continue
        except Exception as e:
            session.rollback()
            print(f"⚠️ Skipping subscription: {e}")
            continue

    try:
        session.commit()
        print(f"✔ Created {created} validated subscriptions")
    except Exception as e:
        session.rollback()
        print(f"❌ Error committing subscriptions: {e}")

def validate_database():
    """Run post-seeding validation checks"""
    print("\nRunning validation checks...")

    customer_count = session.query(Customer).count()
    plan_count = session.query(Plan).count()
    sub_count = session.query(Subscription).count()

    print(f"Customers: {customer_count} | Plans: {plan_count} | Subscriptions: {sub_count}")

    # Detect orphaned subscriptions
    orphaned_subs = session.query(Subscription).filter(
        (Subscription.customer_id.notin_(session.query(Customer.id))) |
        (Subscription.plan_id.notin_(session.query(Plan.id)))
    ).count()

    if orphaned_subs:
        print(f"❌ Found {orphaned_subs} orphaned subscriptions")
    else:
        print("✔ No orphaned subscriptions found")

# ========== Main ==========
def main():
    print("\n=== SEEDING DATABASE WITH VALIDATED FAKE DATA ===")

    try:
        clear_existing_data()
        plans = create_plans()
        customers = create_customers()

        if not plans or not customers:
            raise RuntimeError("Failed to create base data")

        create_subscriptions(customers, plans)
        validate_database()

        print("\n✅ Database seeded and validated successfully!")
    except Exception as e:
        print(f"\n❌ Critical error during seeding: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
