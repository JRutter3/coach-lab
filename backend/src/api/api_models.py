"""
API Models showing what we expect from the front-end
"""

from enum import StrEnum, auto
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, EmailStr, Field

type LowercaseEmail = Annotated[
    EmailStr,
    BeforeValidator(lambda v: v.lower() if isinstance(v, str) else v),
]


##### Canvas Models #####
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


##### User Models #####
class UserSubmission(BaseModel):
    first_name: str
    last_name: str
    e_mail: LowercaseEmail


class StoredUser(UserSubmission):
    user_id: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    e_mail: LowercaseEmail | None = None
