from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from starlette.requests import Request

from queueball.api.utils import get_current_user
from queueball.db import User, Team

router = APIRouter(prefix="/v1")


class ProfileResponse(BaseModel):
    firstName: str
    presignedProfileUrl: HttpUrl | None


class ProfilePictureUploadLinkResponse(BaseModel):
    uploadUrl: HttpUrl


def get_profile_helper(request: Request, user: int | User) -> ProfileResponse:
    session: Session = request.state.session

    if isinstance(user, int):
        user = session.get(User, user)
        if user is None:
            raise HTTPException(
                status_code=404, detail="No user found with the specified ID."
            )

    res = ProfileResponse(firstName=user.first_name, presignedProfileUrl=None)
    if user.profile_picture is not None:
        # TODO render it
        pass
    return res


@router.get("/profile")
async def retrieve_user_profile(request: Request) -> ProfileResponse:
    """Retrieve the current profile of the user based on the auth0 user id."""
    current_user = get_current_user(request)
    return get_profile_helper(request, current_user)


@router.get("/profile-picture-upload-link")
async def retrieve_profile_picture_upload_link(request: Request):
    pass


@router.delete("/profile-picture")
async def delete_profile_picture(request: Request):
    pass


@router.put("/queue")
async def get_in_line(request: Request, hall_id: int, team_id: int | None = None):
    session: Session = request.state.session
    user = get_current_user(request)
    if team_id is None:
        team_id = session.execute(select(Team.id).where(Team.player1_id == user.id).where(Team.player2_id == None)).one()
    query = """
INSERT INTO lines (hall_id, team_id, position)
SELECT
    :hall_id,
    :team_id,
    COALESCE(
        (SELECT MAX(position) + 1 FROM lines WHERE hall_id = :hall_id AND team_id = :team_id),
        1
    )
    """
    session.execute(text(query), {"team_id": team_id, "hall_id": hall_id})
    session.commit()
    return None
