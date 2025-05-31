#!/usr/bin/env python3

from datetime import datetime, timedelta
from models import Session
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription
from sqlalchemy.exc import IntegrityError

session = Session()

def create_unique_email(base="test"):
    """Generate unique test emails"""
    return f"{base}+{datetime.now().microsecond}@example.com"

def create_plan_with_limited_capacity(name, max_customers):
    """Create a plan that's almost full (for testing capacity limits)"""
    try:
        plan = Plan.create(
            name=f"TEST-LIMITED-{name}",
            description=f"Test {name} plan (max {max_customers})",
            price=9.99,
            speed="10 Mbps",
            duration_months=1
        )
        
        if not plan or not plan.id:
            raise ValueError("Failed to create plan")
        
        # Create subscriptions to make it nearly full
        for i in range(max_customers - 1):  # One slot left
            try:
                customer = Customer.create(
                    router_id=f"TEST-LIMITED-{i}-{datetime.now().microsecond}",
                    name=f"Test User {i}",
                    email=create_unique_email(f"user{i}"),
                    phone=f"123456{i:04d}",
                    address=f"{i} Test St"
                )
                
                if not customer or not customer.id:
                    print(f"⚠️ Failed to create customer {i}, skipping")
                    continue
                
                Subscription.create(
                    customer_id=customer.id,
                    plan_id=plan.id,
                    router_id=customer.router_id,
                    start_date=datetime.now() - timedelta(days=1),
                    status="active"
                )
            except IntegrityError as e:
                session.rollback()
                print(f"⚠️ Skipping duplicate customer {i}: {e}")
                continue
        
        session.commit()
        return plan
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating limited plan: {e}")
        raise

def create_expired_subscriptions():
    """Create subscriptions in various expired states"""
    try:
        plans = [
            Plan.create(
                name=f"TEST-EXPIRED-{datetime.now().microsecond}",
                description="Test expired plan",
                price=9.99,
                speed="10 Mbps",
                duration_months=1
            ),
            Plan.create(
                name=f"TEST-ALMOST-EXPIRED-{datetime.now().microsecond}",
                description="Test nearly expired plan",
                price=9.99,
                speed="10 Mbps", 
                duration_months=1
            )
        ]
        
        # Fully expired subscription
        customer1 = Customer.create(
            router_id=f"TEST-EXPIRED-{datetime.now().microsecond}",
            name="Expired User",
            email=create_unique_email("expired"),
            phone="1111111111",
            address="123 Expired St"
        )
        Subscription.create(
            customer_id=customer1.id,
            plan_id=plans[0].id,
            router_id=customer1.router_id,
            start_date=datetime.now() - timedelta(days=60),
            end_date=datetime.now() - timedelta(days=30),
            status="expired"
        )
        
        # Subscription expiring tomorrow
        customer2 = Customer.create(
            router_id=f"TEST-EXPIRING-{datetime.now().microsecond}",
            name="Expiring Soon User",
            email=create_unique_email("expiring"),
            phone="2222222222",
            address="456 Expiring Rd"
        )
        Subscription.create(
            customer_id=customer2.id,
            plan_id=plans[1].id,
            router_id=customer2.router_id,
            start_date=datetime.now() - timedelta(days=29),
            end_date=datetime.now() + timedelta(days=1),
            status="active"
        )
        
        session.commit()
        return plans
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating expired subscriptions: {e}")
        raise

def main():
    print("=== CREATING TEST DATA FOR EDGE CASES ===")
    
    try:
        # Create a plan with only 1 slot remaining
        limited_plan = create_plan_with_limited_capacity("BUSY", max_customers=10)
        print(f"✔ Created nearly-full plan: {limited_plan.name}")
        
        # Create expired/expiring subscriptions
        expired_plans = create_expired_subscriptions()
        print(f"✔ Created test plans with expiring subscriptions")
        
        print("\n✅ Test data created successfully!")
        print("Use these for testing:")
        print("- Plan capacity limits (try adding one more customer)")
        print("- Subscription expiration logic")
        print("- Renewal workflows")
    except Exception as e:
        print(f"\n❌ Failed to create test data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()