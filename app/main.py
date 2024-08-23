import logging
from fastapi import FastAPI

from app.core.exception_handlers import register_exception_handlers
from app.core.logging_config import setup_logging
from app.middlewares.jwt_middleware import JWTMiddleware
from app.users.exception_handler import database_query_exception_handler, user_not_found_exception_handler, \
    handle_email_already_registered, user_profile_update_exception_handler
from app.users.routers import router as user_routes
from app.authentication.routers import router as auth_routes
from app.users.exceptions import EmailAlreadyRegistered, UserNotFoundException, UserProfileUpdateException, \
    DatabaseQueryException

import uvicorn

# Initialize logging
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI()
app.add_exception_handler(DatabaseQueryException, database_query_exception_handler)
app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
app.add_exception_handler(EmailAlreadyRegistered, handle_email_already_registered)
app.add_exception_handler(UserProfileUpdateException, user_profile_update_exception_handler)
# register_exception_handlers(app)
setup_logging()

# Middleware setup
app.add_middleware(JWTMiddleware, whitelist=["/user/signup", "/auth/login", "/auth/healthz", "/docs", "/redoc", "/openapi.json"])

# Include the user router
app.include_router(user_routes, prefix="/user")
app.include_router(auth_routes, prefix="/auth")


@app.on_event("startup")
def on_startup():
    """
    Event handler for application startup.
    """
    logger.info("Application startup completed.")


@app.on_event("shutdown")
def on_shutdown():
    """
    Event handler for application shutdown.
    """
    logger.info("Application shutdown completed.")


# Main entry point to run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    logger.info("Server started.")
