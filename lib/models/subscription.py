from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from . import Base, session
from datetime import date

class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    router_id = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(String, default='active')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    customer = relationship("Customer", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")

    @classmethod
    def create(cls, customer_id, plan_id, router_id, start_date, end_date=None, status='active'):
        try:
            subscription = cls(
                customer_id=customer_id,
                plan_id=plan_id,
                router_id=router_id,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            session.add(subscription)
            session.commit()
            return subscription
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating subscription: {e}")
            return None

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_customer(cls, customer_id):
        return session.query(cls).filter_by(customer_id=customer_id).all()

    @classmethod
    def filter_by_status(cls, status):
        return session.query(cls).filter_by(status=status).all()

    @classmethod
    def update(cls, id, **kwargs):
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
            print(f"❌ Error updating subscription: {e}")
            return None

    @classmethod
    def delete(cls, id):
        try:
            sub = cls.find_by_id(id)
            if sub:
                session.delete(sub)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error deleting subscription: {e}")
            return False

    @property
    def days_left(self):
        if self.end_date:
            return (self.end_date - date.today()).days
        return None

    @property
    def is_expired(self):
        return self.days_left is not None and self.days_left < 0

    def __repr__(self):
        return f"<Subscription {self.id}: Customer {self.customer_id}, Plan {self.plan_id}, Status {self.status}>"

    def __str__(self):
        return f"Sub#{self.id}: {self.customer.name} on {self.plan.name} | Status: {self.status} | Ends: {self.end_date}"
