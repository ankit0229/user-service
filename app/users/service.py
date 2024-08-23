import logging

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.security import get_password_hash
from app.users.models import User
from app.users.schemas import UserUpdate, UserCreate

from app.users.exceptions import EmailAlreadyRegistered, UserNotFoundException, UserProfileUpdateException, \
    DatabaseQueryException

logger = logging.getLogger(__name__)


class UserProfileService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate):
        """
        Create a new user in the database.

        :param user_data: UserCreate schema containing user registration data.
        :return: The newly created User object.
        """
        try:
            if User.get_by_email(self.db, user_data.email):
                raise EmailAlreadyRegistered("This email is already registered.")

            hashed_password = get_password_hash(user_data.password)
            new_user = User(
                email=user_data.email,
                name=user_data.name,
                address=user_data.address,
                date_of_birth=user_data.date_of_birth,
                hashed_password=hashed_password,
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error while creating user: {str(e)}", exc_info=True)
            raise EmailAlreadyRegistered("This email is already registered.")
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"SQLAlchemy error while creating user: {str(e)}", exc_info=True)
            raise DatabaseQueryException("An error occurred while creating a new user.")

    def get_user_by_id(self, user_id: int):
        """
        Retrieve a user by their ID.

        :param user_id: The ID of the user to retrieve.
        :return: The User object if found.
        """
        user = User.get_by_id(self.db, user_id)
        if not user:
            raise UserNotFoundException("User not found with ID: {}".format(user_id))
        return user

    def update_user_profile(self, user_id: int, profile_data: UserUpdate):
        """
         Update the profile of an existing user.

         :param user_id: The ID of the user to update.
         :param profile_data: UserUpdate schema containing the updated profile data.
         :return: The updated User object.
        """
        user = self.get_user_by_id(user_id)  # Using the improved get_by_id method
        try:
            if profile_data.name is not None:
                user.name = profile_data.name
            if profile_data.address is not None:
                user.address = profile_data.address
            if profile_data.date_of_birth is not None:
                user.date_of_birth = profile_data.date_of_birth

            self.db.commit()
            self.db.refresh(user)
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"SQLAlchemy error while updating user: {str(e)}", exc_info=True)
            raise DatabaseQueryException("An error occurred while creating a new user.")
        except Exception as e:
            self.db.rollback()
            raise UserProfileUpdateException(f"Failed to update user profile: {str(e)}")
        return user
