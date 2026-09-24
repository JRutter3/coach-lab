from typing import Annotated

from database.db_tools import db_session_manager
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession


async def db_session(request: Request):
    async with db_session_manager(request.app.state.db_engine) as sess:
        yield sess

type DBSession = Annotated[AsyncSession, Depends(db_session)]