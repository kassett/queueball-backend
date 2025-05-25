from fastapi import FastAPI
from starlette.requests import Request
from sqlalchemy.orm import Session

from queueball.api.versions import v1
from queueball.config import env_vars
from queueball.db import User

settings = env_vars()
session = env_vars().session

app = FastAPI(
    title="QueueBall API",
    description="Endpoints for interacting with QueueBall. "
    "All endpoints are protected by SuperTokens.",
)

app.include_router(router=v1.router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """Create a new database session for each request.

    Context manager ensures session is closed after the thread finishes.
    """

    with session() as request_rw_session:
        request.state.session = request_rw_session

        return await call_next(request)


# @app.middleware("http")
async def add_or_create_user(request: Request, call_next):
    """Add the current user to the context.

    However, if the current user does not exist in the database,
    then create a user record for them
    """
    # # TODO figure out what the appropriate header is
    # jwt = request.headers.get("Bearer")
    # if jwt is None:
    #     return {"statusCode": 401}
    #
    #
    # sess: Session = request.state.session
    # user = sess.get(User, jwt["sub"])
    # if user is None
