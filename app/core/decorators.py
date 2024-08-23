def exception_handler(exception_class):
    def decorator(handler_func):
        handler_func.__exception_class__ = exception_class
        return handler_func
    return decorator
