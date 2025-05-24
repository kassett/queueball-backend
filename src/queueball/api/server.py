from fastapi import FastAPI
from starlette.requests import Request

from queueball.api.versions import v1
from queueball.config import env_vars

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
