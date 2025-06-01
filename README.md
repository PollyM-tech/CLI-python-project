# 🌐 PLY ISP Management CLI

- A command-line tool for managing internet service customers, subscription plans, and billing. Designed using SQLAlchemy ORM and Python, this app supports CRUD operations for Customers, Plans, and Subscriptions.

## Features

- Customer management (Create, Read, Update, Delete)
- Internet plan management (Create, Read, Update, Delete)
- Subscription management (Create, View, Update, Delete)
- Clear and modular CLI menus
- Built-in validations for data integrity
- Realistic data seeding using Faker

## Requirements
Python 3.8+

## Database Schema

Visualize the schema at:  
🔗 [DB Diagram](https://dbdiagram.io/d/CLI-Internet-Service-Manager-68343a530240c65c4438b599)

**Tables & Relationships**:
- `Customer` (one-to-many) → `Subscription`
- `Plan` (one-to-many) → `Subscription`

## 🛠 Technologies & Dependencies

This app uses a virtual environment via **Pipenv**.

### Tech Stack & Dependencies
| Dependency              | Purpose                         |
| ----------------------- | ------------------------------- |
| `SQLAlchemy`            | ORM and schema definition       |
| `Alembic`               | Schema migration tool           |
| `Faker`                 | Generate realistic seed data    |
| `python-dotenv`         | Environment variable management |
| `python-dateutil`       | Flexible datetime parsing       |
| `tabulate` *(optional)* | Pretty-print tables in CLI      |
| `ipdb` *(dev)*          | Debugging tool                  |


## Setup Instructions
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/cli-internet-service-manager.git
   cd cli-internet-service-manager

2. Create virtual environment
pipenv install
pipenv shell

3. Seed the database 
python lib/seed.py

4. Run the application
python lib/cli.py

## 👤 Sample Users
Seeded by default using Faker. Example:
Pauline Moraa
Linus Wafula
Daniel Lumumba

 ## Testing
 python lib/test_database.py

 # Project Structure 
 .
├── Pipfile          
├── README.md                      
└── lib/
    ├── cli.py                     
    ├── seed.py                    
    ├── test_database.py           
    ├── models/
    │   ├── __init__.py
    │   ├── customer.py
    │   ├── plan.py
    │   └── subscription.py
    └── helpers/
        ├── __init__.py
        ├── shared_helpers.py
        ├── customer_helpers.py
        ├── plan_helpers.py
        └── subscription_helpers.py


## Licence
Pauline Moraa


