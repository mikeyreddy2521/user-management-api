
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database location
DATABASE_URL = "sqlite:///./users.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for database tables
Base = declarative_base()
