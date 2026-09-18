from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The connection string format: dialect+driver://user:password@host:port/dbname
# We use localhost because the Python script is running on your Windows machine,
# reaching into the exposed 5432 port of the Docker container.
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:secretpassword@localhost:5432/dog_dispatch"

# The engine is the core interface to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal creates individual, temporary connections for each API request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class for all future table models
Base = declarative_base()

# Dependency function to generate and close database sessions safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()