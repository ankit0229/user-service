from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.users.schemas import UserCreate, UserProfile, UserUpdate
from app.users.service import UserProfileService


router = APIRouter()


@router.post("/signup", response_model=UserProfile)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
        Create a new user in the system.

        Parameters:
        - user: UserCreate - a Pydantic model representing the user input data.
        - db: Session - an SQLAlchemy ORM session dependency.

        Returns:
        - UserProfile: the newly created user profile.

        This endpoint handles user registration, taking necessary user details
        (like email, name, and password) and creating a new user record in the database.
        """
    user_service = UserProfileService(db)
    new_user = user_service.create_user(user)
    return new_user


@router.get("/profile", response_model=UserProfile)
def view_profile(request: Request, db: Session = Depends(get_db)):
    """
    Retrieve the profile information of the currently authenticated user.

    Parameters:
    - request: Request - the request object, used here to access user state.
    - db: Session - an SQLAlchemy ORM session dependency.

    Returns:
    - UserProfile: the user's profile information.

    This endpoint retrieves the profile of the user who made the request,
    identified through authentication middleware that populates `request.state.user`.
    """
    user_info = request.state.user
    user_profile_service = UserProfileService(db)
    return user_profile_service.get_user_by_id(user_info["user_id"])


@router.put("/profile", response_model=UserProfile)
def update_profile(request: Request, profile_data: UserUpdate, db: Session = Depends(get_db)):
    """
       Update the profile information of the currently authenticated user.

       Parameters:
       - request: Request - the request object, used to access user state.
       - profile_data: UserUpdate - a Pydantic model containing the data for profile updates.
       - db: Session - an SQLAlchemy ORM session dependency.

       Returns:
       - UserProfile: the updated user profile.

       This endpoint allows the user to update their profile information
       (like name, address, date of birth). The user is identified through the authentication
       middleware that ensures they are logged in and populates `request.state.user`.
    """
    user_profile_service = UserProfileService(db)
    user_info = request.state.user
    updated_user = user_profile_service.update_user_profile(user_info["user_id"], profile_data)
    return updated_user
