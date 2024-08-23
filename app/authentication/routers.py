import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.authentication.schemas import Token, HealthCheck
from app.authentication.service import AuthService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/healthz", response_model=HealthCheck)
def healthz():
    return {"message": "Service is up and running"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and issue a JWT token upon successful login.

    :param form_data: OAuth2PasswordRequestForm which includes username and password.
    :param db: SQLAlchemy session dependency for database access.
    :return: A dictionary containing the access token and token type.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Unauthorized login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = auth_service.create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
