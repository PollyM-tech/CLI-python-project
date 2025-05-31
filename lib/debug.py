from models import Base, engine, Session  # Import Session from models
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

def reset_db():
    """Reset the database by dropping and recreating all tables"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database reset complete!")

def seed_data():
    """Seed the database with sample data"""
    session = Session()  # Create a new session
    
    try:
        # First clear any existing data
        session.query(Subscription).delete()
        session.query(Customer).delete()
        session.query(Plan).delete()
        session.commit()

        # Create sample plans
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
        
        # Create subscriptions with proper dates
        Subscription.create(
            customer_id=john.id,
            plan_id=basic.id,
            router_id="ROUT001",
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30*12)  # 1 year
        )
        
        Subscription.create(
            customer_id=jane.id,
            plan_id=premium.id,
            router_id="ROUT002",
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30*12)  # 1 year
        )
        
        print("Sample data seeded successfully!")
    except IntegrityError as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    reset_db()
    seed_data()