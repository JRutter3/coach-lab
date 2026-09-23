from typing import Annotated

from api.api_models import CanvasSubmission
from api.dependencies import db_session
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

canvas = APIRouter(tags=["Canvas Routes"], prefix="/api/v1/canvas-drawing")

@canvas.get("/count")
async def get_row_count(
    session: Annotated[AsyncSession, Depends(db_session)]
) -> int:
    """Post the passed canvas to the database"""
    row_count = await session.execute(text("SELECT COUNT(*) FROM canvases"))
    print(f"Row count: {row_count}")
    return row_count.first()[0]

@canvas.post("/")
async def post_canvas(
    canvas_data: CanvasSubmission,
    session: Annotated[AsyncSession, Depends(db_session)]
) -> str:
    """Post the passed canvas to the database"""
    print("Hello world")

@canvas.get("/{canvas_id}")
async def get_canvas(canvas_id: str) -> CanvasSubmission: ...


@canvas.put("/{canvas_id}")
async def put_canvas(canvas_id: str) -> CanvasSubmission: ...