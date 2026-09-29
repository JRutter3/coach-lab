from typing import Annotated, Any

from config.config_models import APIConfig
from config.config_parser import get_config
from database.db_tools import db_session_manager
from fastapi import Cookie, Depends, HTTPException, Request
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession


async def db_session(request: Request):
    async with db_session_manager(request.app.state.db_engine) as sess:
        yield sess

def require_auth(
    cfg: Annotated[APIConfig, Depends(get_config)],
    token: str | None = Cookie(default=None)
) -> dict[str, Any]:
    """Dependency that ensures the frontend has passed a valid token."""
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = jwt.decode(
            token,
            cfg.jwt_settings.secret_key,
            algorithms=[cfg.jwt_settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Unauthorized")


type DBSession = Annotated[AsyncSession, Depends(db_session)]
type AuthData = Annotated[dict[str, Any], Depends(require_auth)]
