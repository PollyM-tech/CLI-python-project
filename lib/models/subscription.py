from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base, session

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    plan_id = Column(Integer, ForeignKey('plans.id'))
    router_id = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default='active')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    
    # ORM Methods
    @classmethod
    def create(cls, customer_id, plan_id, router_id, start_date, end_date=None, status='active'):
        """Create a new subscription"""
        try:
            new_sub = cls(
                customer_id=customer_id,
                plan_id=plan_id,
                router_id=router_id,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            session.add(new_sub)
            session.commit()
            return new_sub
        except Exception as e:
            session.rollback()
            print(f"Error creating subscription: {e}")
            return None
    
    @classmethod
    def get_all(cls):
        """Get all subscriptions"""
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, id):
        """Find subscription by ID"""
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_customer(cls, customer_id):
        """Find all subscriptions for a customer"""
        return session.query(cls).filter_by(customer_id=customer_id).all()
    
    @classmethod
    def find_active_by_customer(cls, customer_id):
        """Find active subscriptions for a customer"""
        return session.query(cls).filter_by(
            customer_id=customer_id,
            status='active'
        ).all()
    
    @classmethod
    def find_by_plan(cls, plan_id):
      """Find all subscriptions for a specific plan"""
      return session.query(cls).filter_by(plan_id=plan_id).all()
    
    @classmethod
    def update(cls, id, **kwargs):
        """Update subscription attributes"""
        try:
            sub = cls.find_by_id(id)
            if sub:
                for key, value in kwargs.items():
                    setattr(sub, key, value)
                session.commit()
                return sub
            return None
        except Exception as e:
            session.rollback()
            print(f"Error updating subscription: {e}")
            return None
    
    @classmethod
    def delete(cls, id):
        """Delete a subscription"""
        try:
            sub = cls.find_by_id(id)
            if sub:
                session.delete(sub)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting subscription: {e}")
            return False
    
    def __repr__(self):
        return f"<Subscription {self.id}: Customer {self.customer_id} - Plan {self.plan_id} ({self.status})>"