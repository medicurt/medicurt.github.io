from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
#Creates the DB connection session which hosts the CRUD transactions between the program and the db

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping = True, future = True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)