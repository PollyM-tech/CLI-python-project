from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from . import Base, session
from sqlalchemy.orm import relationship


class Plan(Base):
    __tablename__ = 'plans'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))
    speed = Column(String)
    duration_months = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    subscriptions = relationship("Subscription", back_populates="plan")

    # ORM Methods
    @classmethod
    def create(cls, name, description, price, speed, duration_months):
        """Create a new plan"""
        try:
            new_plan = cls(
                name=name,
                description=description,
                price=price,
                speed=speed,
                duration_months=duration_months
            )
            session.add(new_plan)
            session.commit()
            return new_plan
        except Exception as e:
            session.rollback()
            print(f"Error creating plan: {e}")
            return None
    
    @classmethod
    def get_all(cls):
        """Get all plans"""
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, id):
        """Find plan by ID"""
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def find_by_name(cls, name):
        """Find plan by name"""
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
    
    @classmethod
    def update(cls, id, **kwargs):
        """Update plan attributes"""
        try:
            plan = cls.find_by_id(id)
            if plan:
                for key, value in kwargs.items():
                    setattr(plan, key, value)
                session.commit()
                return plan
            return None
        except Exception as e:
            session.rollback()
            print(f"Error updating plan: {e}")
            return None
    
    @classmethod
    def delete(cls, id):
        """Delete a plan"""
        try:
            plan = cls.find_by_id(id)
            if plan:
                session.delete(plan)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"Error deleting plan: {e}")
            return False
    
    def __repr__(self):
        return f"<Plan {self.id}: {self.name} ({self.speed}) - ${self.price}/month>"