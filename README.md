# 🌐 PLY ISP Management CLI

- A command-line application to manage internet customers, plans, and subscriptions — built with Python and SQLAlchemy ORM. Designed for small to mid-size ISPs or simulations, the app features CRUD functionality, relational integrity, and a clean modular CLI interface.


## Features

- **Customer Management** — Add, view, update, and delete users
- **Internet Plans** — Define, modify, or remove service tiers
- **Subscriptions** — Link customers to plans with start/end dates and status
- **Status Filtering** — Quickly filter subscriptions by `active`, `expired`, etc.
- **Expiring Alerts** — View subscriptions ending within 30 days
- **Data Validations** — Email, phone, router ID checks built-in
- **Realistic Seeding** — Auto-generates realistic data using Faker


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
   cd cli-internet-service-manager

2. Create virtual environment
pipenv install
pipenv shell

3. Seed the database 
python lib/seed.py

4. Run the application
python lib/cli.py

## 👤 Sample Users
generated with random details

 ## Testing
 python lib/test_database.py it includes:

- Entity counts

- Orphan detection

- Relationship test (Customer ↔ Subscription)

- Unique constraint checks

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

## Future Improvements
- Invoice tracking

- Payment history

- Role-based user authentication (admin vs staff)

- Export reports (CSV or PDF)

- Web version via Flask or FastAPI

## Licence
Pauline Moraa


