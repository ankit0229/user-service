def exception_handler(exception_class):
    """
    A decorator function that attaches an exception class to a handler function.

    :param exception_class: The class of the exception to be handled by the decorated function.
    :return: A decorator that adds an `__exception_class__` attribute to the handler function.
    """
    def decorator(handler_func):
        handler_func.__exception_class__ = exception_class
        return handler_func
    return decorator
