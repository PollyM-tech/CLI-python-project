from models import *
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

def reset_db():
    """Reset the database by dropping and recreating all tables"""
    # Get the engine from models/__init__.py
    from models import engine
    Base.metadata.drop_all(engine)  # Add engine as bind parameter
    Base.metadata.create_all(engine)
    print("Database reset complete!")

def seed_data():
    """Seed the database with sample data"""
    # Create sample plans
    try:
        basic = Plan.create(
            name="Basic",
            description="Entry-level internet",
            price=29.99,
            speed="50 Mbps",
            duration_months=12
        )
        
        premium = Plan.create(
            name="Premium",
            description="High-speed internet",
            price=59.99,
            speed="200 Mbps",
            duration_months=12
        )
        
        # Create sample customers
        john = Customer.create(
            router_id="ROUT001",
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St"
        )
        
        jane = Customer.create(
            router_id="ROUT002",
            name="Jane Smith",
            email="jane@example.com",
            phone="0987654321",
            address="456 Oak Ave"
        )
        
        # Create subscriptions
        Subscription.create(
            customer_id=john.id,
            plan_id=basic.id,
            router_id="ROUT001",
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=365)
        )
        
        Subscription.create(
            customer_id=jane.id,
            plan_id=premium.id,
            router_id="ROUT002",
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=365)
        )
        
        print("Sample data seeded successfully!")
    except IntegrityError as e:
        print(f"Error seeding data: {e}")

if __name__ == "__main__":
    reset_db()
    seed_data()