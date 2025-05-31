from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# Configure your database connection
engine = create_engine('sqlite:///internet_service_manager.db')
Session = sessionmaker(bind=engine)
session = Session()

def create_tables():
    Base.metadata.create_all(bind=engine)

# Export these for use in other files
__all__ = ['Base', 'engine', 'session', 'create_tables']

# Import models to register them with SQLAlchemy
from .customer import Customer
from .plan import Plan
from .subscription import Subscription