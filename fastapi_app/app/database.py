from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL Connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:new_password@localhost:5432/postgres"

# Create database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

