from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.sql import func


from app.db.base import Base


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    street_address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state_or_province = Column(String, nullable=False)
    country = Column(String, nullable=False)
    date_to_occur = Column(DateTime, nullable=False)
    recurring = Column(Boolean, nullable=True)
    # If no admission fee entered, schema defaults value to 0
    admission_fee = Column(Float, nullable=False)
    is_open = Column(Boolean, nullable=False)
    max_participants = Column(Integer, nullable=True)
    sort_order = Column(Integer, nullable = False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    created_by = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
