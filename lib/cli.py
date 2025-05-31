#!/usr/bin/env python3

from helpers import (
    clear_screen,
    exit_program,
    # Customer functions
    list_customers,
    create_customer,
    find_customer_by_email,
    update_customer,
    delete_customer,
    # Plan functions
    list_plans,
    create_plan,
    find_plan_by_name,
    update_plan,
    delete_plan,
    # Subscription functions
    list_subscriptions,
    create_subscription,
    find_subscriptions_by_customer,
    update_subscription_status
)

def main():
    clear_screen()
    print("=== INTERNET SERVICE MANAGER ===")
    while True:
        main_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            exit_program()
        elif choice == "1":
            customer_menu()
        elif choice == "2":
            plan_menu()
        elif choice == "3":
            subscription_menu()
        else:
            print("Invalid choice. Please try again.")

def main_menu():
    print("\nMAIN MENU")
    print("1. Customer Management")
    print("2. Plan Management")
    print("3. Subscription Management")
    print("0. Exit")

def customer_menu():
    while True:
        print("\nCUSTOMER MANAGEMENT")
        print("1. List all customers")
        print("2. Add new customer")
        print("3. Find customer by email")
        print("4. Update customer")
        print("5. Delete customer")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            list_customers()
        elif choice == "2":
            create_customer()
        elif choice == "3":
            find_customer_by_email()
        elif choice == "4":
            update_customer()
        elif choice == "5":
            delete_customer()
        else:
            print("Invalid choice. Please try again.")

def plan_menu():
    while True:
        print("\nPLAN MANAGEMENT")
        print("1. List all plans")
        print("2. Add new plan")
        print("3. Find plan by name")
        print("4. Update plan")
        print("5. Delete plan")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            list_plans()
        elif choice == "2":
            create_plan()
        elif choice == "3":
            find_plan_by_name()
        elif choice == "4":
            update_plan()
        elif choice == "5":
            delete_plan()
        else:
            print("Invalid choice. Please try again.")

def subscription_menu():
    while True:
        print("\nSUBSCRIPTION MANAGEMENT")
        print("1. Create new subscription")
        print("2. List all subscriptions")
        print("3. Find subscriptions by customer")
        print("4. Update subscription status")
        print("0. Back to main menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            create_subscription()
        elif choice == "2":
            list_subscriptions()
        elif choice == "3":
            find_subscriptions_by_customer()
        elif choice == "4":
            update_subscription_status()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()