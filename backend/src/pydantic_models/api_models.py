"""
API Models showing what we expect from the front-end
"""

from enum import StrEnum, auto
from typing import Literal

from pydantic import BaseModel, Field


class CanvasTemplateEnum(StrEnum):
    FULL_HOCKEY_RINK = auto()
    HALF_HOCKEY_RINK = auto()

class CanvasShapeEnum(StrEnum):
    CIRCLE = auto()
    X_MARK = auto()
    PYLON = auto()


class LinesType(BaseModel):
    tool: Literal["brush"]
    points: list[float]

class Coordinates(BaseModel):
    x: float
    y: float

class ShapesType(BaseModel):
    tool: CanvasShapeEnum
    location: Coordinates

class CanvasSubmission(BaseModel):
    template:  CanvasTemplateEnum
    lines: list[LinesType]
    shapes: list[ShapesType] = Field(default_factory=list)


