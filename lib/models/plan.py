from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from . import Base, session

class Plan(Base):
    __tablename__ = 'plans'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    speed = Column(String, nullable=False)
    duration_months = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    subscriptions = relationship("Subscription", back_populates="plan", cascade="all, delete-orphan")

    @classmethod
    def create(cls, name, description, price, speed, duration_months):
        existing = session.query(cls).filter_by(name=name).first()
        if existing:
            print(f"❌ Plan with name '{name}' already exists.")
            return None
        try:
            plan = cls(
                name=name,
                description=description,
                price=price,
                speed=speed,
                duration_months=duration_months
            )
            session.add(plan)
            session.commit()
            return plan
        except IntegrityError:
            session.rollback()
            print("❌ Integrity Error: Plan with this name already exists.")
            return None
        except Exception as e:
            session.rollback()
            print(f"❌ Error creating plan: {e}")
            return None

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()

    @classmethod
    def update(cls, id, **kwargs):
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
            print(f"❌ Error updating plan: {e}")
            return None

    @classmethod
    def delete(cls, id):
        try:
            plan = cls.find_by_id(id)
            if plan:
                session.delete(plan)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ Error deleting plan: {e}")
            return False

    def __repr__(self):
        return f"<Plan {self.id}: {self.name} ({self.speed}) - KES {self.price}/mo>"

    def __str__(self):
        return f"{self.name} – {self.speed}, KES {self.price}/mo, {self.duration_months} mo"
