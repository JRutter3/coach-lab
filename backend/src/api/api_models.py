"""
API Models showing what we expect from the front-end
"""
########################################################################
# NOTE: Pydantic model attribue name MUST match database column names! #
########################################################################

import datetime as dt
from enum import StrEnum, auto
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, BeforeValidator, EmailStr, Field

type LowercaseEmail = Annotated[
    EmailStr,
    BeforeValidator(lambda v: v.lower() if isinstance(v, str) else v),
]


type CoercedUTCDatetime = Annotated[
    AwareDatetime,
    BeforeValidator(lambda d: d.replace(tzinfo=dt.timezone.utc) if isinstance(d, dt.datetime) else d)
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
    email: LowercaseEmail


class StoredUser(UserSubmission):
    id: str


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: LowercaseEmail | None = None


##### Organization Models #####
class OrgSubmission(BaseModel):
    name: str


class StoredOrg(OrgSubmission):
    id: str
    created_at: CoercedUTCDatetime


class OrgUpdate(BaseModel):
    name: str | None  # Because this is the only attribute, it can't be none...
