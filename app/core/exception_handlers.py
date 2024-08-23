from fastapi import FastAPI
import importlib
import pkgutil


def register_exception_handlers(app: FastAPI):
    import app

    # Dynamically import all exception handlers from each module and register them
    package = app
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
        if "exception_handlers" in module_name:
            module = importlib.import_module(module_name)
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                if callable(attribute) and hasattr(attribute, '__exception_class__'):
                    exception_class = getattr(attribute, '__exception_class__')
                    app.add_exception_handler(exception_class, attribute)
                    print(exception_class)
                    print(attribute)

