import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.decorators import exception_handler
from app.users.exceptions import EmailAlreadyRegistered, UserNotFoundException, UserProfileUpdateException, \
    DatabaseQueryException

logger = logging.getLogger(__name__)


@exception_handler(EmailAlreadyRegistered)
async def handle_email_already_registered(request: Request, exc: EmailAlreadyRegistered):
    logging.error("EmailAlreadyRegistered handler triggered")
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "User not found"}
    )


@exception_handler(UserProfileUpdateException)
async def user_profile_update_exception_handler(request: Request, exc: UserProfileUpdateException):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@exception_handler(DatabaseQueryException)
async def database_query_exception_handler(request: Request, exc: DatabaseQueryException):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error - Unable to process the request"}
    )
