from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from app.db.base import Base
from app.users.exceptions import DatabaseQueryException

# Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    address = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    dt_created = Column(DateTime(timezone=True), server_default=func.now())
    dt_updated = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def get_by_id(cls, db_session: Session, user_id: int):
        try:
            return db_session.query(cls).filter(cls.id == user_id).one()
        except NoResultFound:
            return None
        except SQLAlchemyError as e:
            raise DatabaseQueryException("Failed to retrieve user by email", original_exception=e)

    @classmethod
    def get_by_email(cls, db_session: Session, email: str):
        try:
            return db_session.query(cls).filter(cls.email == email).one()
        except NoResultFound:
            return None
        except SQLAlchemyError as e:
            raise DatabaseQueryException("Failed to retrieve user by email", original_exception=e)
