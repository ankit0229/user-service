from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create an SQLAlchemy engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)  # `echo=True` is optional and useful for debugging

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
