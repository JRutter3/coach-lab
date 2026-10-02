from database.db_tools import (
    DataNotFoundError,
    get_user_from_database,
    query_users_by_email,
    update_user_in_database,
    write_user_to_database,
)
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from api.api_models import StoredUser, UserSubmission, UserUpdate
from api.dependencies import AuthData, DBSession

user_router = APIRouter(prefix="/api/v1/users", tags=["User Endpoints"])


@user_router.post("/")
async def post_user(user: UserSubmission, db_session: DBSession) -> StoredUser:
    """Post a new user."""
    try:
        resp = await write_user_to_database(user, db_session)
    except IntegrityError:
        raise HTTPException(
            422,
            f"User with email: {user.email} already exists"
        )
    return resp

@user_router.get("/me")
async def get_user(user_data: AuthData, db_session: DBSession) -> StoredUser:
    """Get a user with the given user_id."""
    user_id = user_data.id
    try:
        resp = await get_user_from_database(user_id, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            detail=f"This is the correct URL, but no user with ID: {user_id} found."
        )
    return resp


@user_router.get("/")  # TODO: Move this to an admin section where only I can use it.
async def query_user(email: str, db_session: DBSession) -> StoredUser:
    """Query user table by email address."""
    try:
        resp = await query_users_by_email(email, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            detail=f"This is the correct URL but no user with email: {email} found."
        )

    return resp

@user_router.put("/{user_id}")
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    session: DBSession
) -> StoredUser:
    """Update the user with new UserUpdate information"""
    try:
        resp = await update_user_in_database(user_id, user_update, session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            detail= (
                f"This is the correct URL"
                f", but no user with ID: {user_id} found."
            )
        )

    return resp