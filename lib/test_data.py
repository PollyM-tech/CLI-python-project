from models import session
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription

def run_database_tests():
    print("\n🔍 Running database integrity tests...")

    # Count checks
    total_customers = session.query(Customer).count()
    total_plans = session.query(Plan).count()
    total_subscriptions = session.query(Subscription).count()

    print(f"👤 Customers:           {total_customers}")
    print(f" Internet Plans:      {total_plans}")
    print(f" Subscriptions:       {total_subscriptions}")

    # Sample customer relationship check
    print("\n🔗 Testing relationships...")
    sample_customer = session.query(Customer).first()
    if sample_customer:
        print(f"✅ Sample Customer: {sample_customer.name} ({sample_customer.email})")
        for sub in sample_customer.subscriptions:
            print(f"  ↳ Subscribed to {sub.plan.name} | Status: {sub.status} | Ends: {sub.end_date}")
    else:
        print("⚠️  No customers found to test subscriptions.")

    # Orphaned subscriptions (no customer or plan)
    orphans = session.query(Subscription).filter(
        ~Subscription.customer.has() | ~Subscription.plan.has()
    ).count()

    print(f"\n Orphaned Subscriptions: {orphans}")
    if orphans == 0:
        print("✅ All subscriptions are correctly linked to customers and plans.")
    else:
        print("❌ Some subscriptions are missing relationships!")

    # Email and router ID uniqueness
    print("\n🔍 Checking for duplicate or missing fields...")
    missing_routers = session.query(Customer).filter((Customer.router_id == None) | (Customer.router_id == '')).count()
    missing_emails = session.query(Customer).filter((Customer.email == None) | (Customer.email == '')).count()

    duplicates_email = session.query(Customer.email).group_by(Customer.email).having(
        session.query(Customer).filter(Customer.email == Customer.email).count() > 1
    ).count()

    print(f"✉️  Customers without email: {missing_emails}")
    print(f" Customers without router_id: {missing_routers}")
    if duplicates_email:
        print("❌ Duplicate emails found!")
    else:
        print("✅ All emails appear unique.")

    print("\n✅ Database integrity test complete.\n")

if __name__ == "__main__":
    run_database_tests()
