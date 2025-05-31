from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base, session

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    router_id = Column(String, unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    address = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationship
    subscriptions = relationship("Subscription", back_populates="customer")
    
    # ORM Methods
    @classmethod
    def create(cls, router_id, name, email, phone, address):
        """Create a new customer"""
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
            print(f"Error creating customer: {e}")
            return None
    
    @classmethod
    def get_all(cls):
        """Get all customers"""
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, id):
        """Find customer by ID"""
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_email(cls, email):
        """Find customer by email"""
        return session.query(cls).filter_by(email=email).first()
    
    @classmethod
    def find_by_router_id(cls, router_id):
        """Find customer by router ID"""
        return session.query(cls).filter_by(router_id=router_id).first()
    
    @classmethod
    def update(cls, id, **kwargs):
        """Update customer attributes"""
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
            print(f"Error updating customer: {e}")
            return None
    
    @classmethod
    def delete(cls, id):
        """Delete a customer"""
        try:
            customer = cls.find_by_id(id)
            if customer:
                session.delete(customer)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting customer: {e}")
            return False
    
    def __repr__(self):
        return f"<Customer {self.id}: {self.name} ({self.email})>"