from fastapi import HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session

from queueball.db import User


def get_current_user(request: Request) -> User:
    """Get the current user from the request context."""
    user_id: int = request.state.user_id
    session: Session = request.state.session
    if user_id is None or (user := session.get(User, user_id)) is None:
        raise HTTPException(status_code=401, detail="User is not logged in.")
    return user
