from database.db_tools import (
    DataNotFoundError,
    get_canvas_from_database,
    query_canvas_by_owner,
    update_canvas_in_database,
    write_canvas_to_database,
)
from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from api.api_models import CanvasSubmission, CanvasUpdate, StoredCanvas
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
    row_count = await session.scalar(text("SELECT COUNT(*) FROM canvases"))
    print(f"Row count: {row_count}")
    return row_count

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

@canvas_router.get("/")
async def query_canvas(owner_id: str, db_session: DBSession) -> list[StoredCanvas]:
    """Query all canvases belonging to a specific user."""
    return await query_canvas_by_owner(owner_id, db_session)


@canvas_router.put("/{canvas_id}")
async def put_canvas(
    canvas_id: str,
    canvas_update: CanvasUpdate,
    db_session: DBSession
) -> StoredCanvas:
    """Update a canvas with the latest data."""
    try:
        result = await update_canvas_in_database(canvas_id, canvas_update, db_session)
    except DataNotFoundError:
        raise HTTPException(404, f"No canvas with id: {canvas_id} found.")

    return result