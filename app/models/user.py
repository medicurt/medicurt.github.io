from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, select
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func


from app.db.base import Base
#This model configures the many-to-many association table between users and events
#Users can subscribe to many events and events can have many users subscribed. 
class UserSubscriptions(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    event_id = Column(Integer, ForeignKey("event.id"), nullable = False)

    created_at = Column(DateTime(timezone=True), default=func.now())

#This model configures the user table in the db, which is used to control both access to the API as well as associate users with events.
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    permissions_id = Column(
        Integer, ForeignKey("permissions.id"), nullable=True, index=True
    )
    created_at = Column(DateTime(timezone=True), default=func.now())

