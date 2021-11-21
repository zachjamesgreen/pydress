import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

username = os.environ.get('DB_USERNAME')
host = os.environ.get('DB_HOST')
password = os.environ.get('DB_PASSWORD')
SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{password}@{host}/pydress"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()