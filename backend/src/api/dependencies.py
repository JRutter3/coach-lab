from database.db_tools import db_session_manager
from fastapi import Request


async def db_session(request: Request):
    async with db_session_manager(request.app.state.db_engine) as sess:
        yield sess