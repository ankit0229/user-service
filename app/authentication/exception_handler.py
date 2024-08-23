# # app/core/exception_handlers.py
#
# from fastapi import Request
# from fastapi.responses import JSONResponse
# from .exceptions import JWTError
# from ..core.decorators import exception_handler
#
#
# @exception_handler(JWTError)
# async def jwt_error_handler(request: Request, exc: JWTError):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )
