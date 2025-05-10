"""Main application file for the FastAPI service.

This module initializes the FastAPI application and includes the necessary routers.
"""

from fastapi import FastAPI

from be_task_ca.item.api import item_router
from be_task_ca.user.api import user_router

# from be_task_ca.database import SessionLocal, engine


app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)


# @app.middleware("http")
# async def db_session_middleware(request: Request, call_next):
#     response = Response("Internal server error", status_code=500)
#     try:
#         request.state.db = SessionLocal()
#         response = await call_next(request)
#     finally:
#         request.state.db.close()
#     return response


@app.get("/")
async def root() -> dict:
    """Root endpoint for the API.

    Returns:
        A simple greeting message.
    """
    return {"message": "Thanks for shopping at Nile!"}
