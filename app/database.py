import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"
# DATABASE_URL = "postgresql://postgres:developer@localhost:5432/ecommerce_db"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:developer@localhost:5432/ecommerce_db")


# Set up the database engine
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare a base class for models
Base: DeclarativeMeta = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
