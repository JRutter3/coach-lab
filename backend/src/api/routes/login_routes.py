import datetime as dt
from typing import Annotated

from config.config_models import APIConfig, JWTSettings
from config.config_parser import get_config
from database.db_tools import DataNotFoundError, get_raw_user_by_email
from fastapi import APIRouter, Depends, HTTPException, Response
from jose import jwt

from api.api_models import LoginRequest, MessageResponse
from api.dependencies import DBSession

login_router = APIRouter(prefix="/api/login")

def create_token(
    user_id: str,
    email: str,
    jwt_settings: JWTSettings
) -> str:
    """Create a token to be stored by the frontend."""
    payload = {
        "id": user_id,
        "email": email,
        "exp": dt.datetime.now(tz=dt.UTC) + dt.timedelta(jwt_settings.token_expire_hours)
    }
    return jwt.encode(payload, jwt_settings.secret_key, jwt_settings.jwt_algorithm)


@login_router.post("/")
async def login(
    body: LoginRequest,
    response: Response,
    db_session: DBSession,
    config: Annotated[APIConfig, Depends(get_config)]
) -> MessageResponse:
    try:
        user = await get_raw_user_by_email(body.email, db_session)
    except DataNotFoundError:
        user = None

    if not user or not user.verify_password(body.password):
        raise HTTPException(401, detail="Invalid email or password")

    token = create_token(user.id, user.email, config.jwt_settings)
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * config.jwt_settings.token_expire_hours,
    )

    return MessageResponse(message="Logged in successfully!")

@login_router.post("/logout")
async def logout(response: Response) -> MessageResponse:
    response.delete_cookie("token")
    return MessageResponse(message= "Logged out successfully")