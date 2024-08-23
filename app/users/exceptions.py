class EmailAlreadyRegistered(Exception):
    """Exception raised for attempts to register with an already registered email."""
    pass


class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""
    pass


class UserProfileUpdateException(Exception):
    """Exception raised during the update of a user profile."""
    def __init__(self, message="Failed to update user profile"):
        self.message = message
        super().__init__(self.message)


class DatabaseQueryException(Exception):
    """Exception raised for errors that occur during database query operations."""
    def __init__(self, message="Database query failed", original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception
