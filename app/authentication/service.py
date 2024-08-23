from sqlalchemy.orm import Session
from app.users.models import User
from app.core.security import create_access_token, verify_password
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Authenticate a user by their email and password.

        :param email: The email address of the user.
        :param password: The password provided by the user.
        :return: The authenticated User object if authentication is successful, otherwise None.
        """
        user = User.get_by_email(self.db, email)
        if not user:
            logger.info(f"Authentication failed for non-existent user: {email}")
            return None
        if not verify_password(password, user.hashed_password):
            logger.warning(f"Failed password verification for user: {email}")
            return None
        return user

    def create_user_token(self, user: User) -> str:
        """
        Create a JWT access token for an authenticated user.

        :param user: The authenticated User object.
        :return: A JWT access token for the user.
        """
        access_token_expires = timedelta(minutes=30)
        token = create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )
        logger.info(f"Token created for user ID: {user.id}")
        return token
