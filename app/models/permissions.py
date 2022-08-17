from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from app.db.base import Base

#This table controls the permissions associated with registered users. The JSONB uses an enumerated string type
#to set DENY/READ/READ-WRITE/or FULL privileges for each API endpoint.
class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    description = Column(String)
    permissions = Column(JSONB, nullable=False)

    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
