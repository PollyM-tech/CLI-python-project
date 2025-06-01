# lib/models/customer.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base, session

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    router_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    subscriptions = relationship("Subscription", back_populates="customer", cascade="all, delete-orphan")

    @classmethod
    def create(cls, router_id, name, email, phone, address):
        try:
            new_customer = cls(
                router_id=router_id,
                name=name,
                email=email,
                phone=phone,
                address=address
            )
            session.add(new_customer)
            session.commit()
            return new_customer
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating customer: {e}")
            return None

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_email(cls, email):
        return session.query(cls).filter_by(email=email).first()

    @classmethod
    def update(cls, id, **kwargs):
        try:
            customer = cls.find_by_id(id)
            if customer:
                for key, value in kwargs.items():
                    setattr(customer, key, value)
                session.commit()
                return customer
            return None
        except Exception as e:
            session.rollback()
            print(f"❌ Error updating customer: {e}")
            return None

    @classmethod
    def delete(cls, id):
        try:
            customer = cls.find_by_id(id)
            if customer:
                session.delete(customer)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error deleting customer: {e}")
            return False

    def __repr__(self):
        return f"<Customer {self.id}: {self.name} ({self.email})>"
