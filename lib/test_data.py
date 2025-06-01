from models import session
from models.customer import Customer
from models.plan import Plan
from models.subscription import Subscription

def run_database_tests():
    print("🔍 Running database integrity tests...")

    # Counts
    total_customers = session.query(Customer).count()
    total_plans = session.query(Plan).count()
    total_subscriptions = session.query(Subscription).count()

    print(f"👤 Customers: {total_customers}")
    print(f"Plans: {total_plans}")
    print(f" Subscriptions: {total_subscriptions}")

    # Sample customer and their subscriptions
    sample_customer = session.query(Customer).first()
    if sample_customer:
        print(f"\n✅ Sample Customer: {sample_customer.name} ({sample_customer.email})")
        for sub in sample_customer.subscriptions:
            print(f"  ↳ Subscribed to {sub.plan.name} | Status: {sub.status} | Ends: {sub.end_date}")
    else:
        print("⚠️ No customers found to test relationships.")

    # Check for orphaned subscriptions
    orphans = session.query(Subscription).filter(
        ~Subscription.customer.has(), ~Subscription.plan.has()
    ).count()

    print(f"\n Orphaned subscriptions: {orphans}")
    if orphans == 0:
        print("✔ All subscriptions are properly linked.")
    else:
        print("❌ Some subscriptions are missing linked customers or plans!")

    print("\n✅ Database test complete.\n")

if __name__ == "__main__":
    run_database_tests()
