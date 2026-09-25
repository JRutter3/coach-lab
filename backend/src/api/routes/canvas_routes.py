from database.db_tools import (
    DataNotFoundError,
    get_canvas_from_database,
    write_canvas_to_database,
)
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from api.api_models import CanvasSubmission, StoredCanvas
from api.dependencies import DBSession

canvas_router = APIRouter(
    tags=["Canvas Routes"],
    prefix="/api/v1/canvas-drawing",
)

@canvas_router.get("/count")
async def get_row_count(
    session: DBSession
) -> int:
    """Post the passed canvas to the database"""
    row_count = await session.execute(text("SELECT COUNT(*) FROM canvases"))
    print(f"Row count: {row_count}")
    return row_count.first()[0]

@canvas_router.post("/")
async def post_canvas(
    canvas_data: CanvasSubmission,
    session: DBSession,
) -> StoredCanvas:
    """Post the passed canvas to the database"""
    return await write_canvas_to_database(canvas_data, session)

@canvas_router.get("/{canvas_id}")
async def get_canvas(canvas_id: str, db_session: DBSession) -> StoredCanvas:
    """Get the canvas from the database by id."""
    try:
        result = await get_canvas_from_database(canvas_id, db_session)
    except DataNotFoundError:
        raise HTTPException(404, f"No canvas with id {canvas_id} found.")
    return result

@canvas_router.put("/{canvas_id}")
async def put_canvas(canvas_id: str) -> CanvasSubmission: ...