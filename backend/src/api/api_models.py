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


class UserRoleEnum(StrEnum):  # We reuse this for groups and orgs. Can be separated.
    MEMBER=auto()
    ADMIN=auto()


class MessageResponse(BaseModel):
    message: str

##### Canvas Models #####
class CanvasTemplateEnum(StrEnum):
    FULL_HOCKEY_RINK = auto()
    HALF_HOCKEY_RINK = auto()

class CanvasVisibility(StrEnum):
    PRIVATE=auto()
    GROUP=auto()
    ORG=auto()


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


class CanvasData(BaseModel):
    lines: list[LinesType]
    shapes: list[ShapesType] = Field(default_factory=list)

class CanvasSubmission(BaseModel):
    name: str
    template: CanvasTemplateEnum
    data: CanvasData
    visibility: CanvasVisibility
    group_id: str | None = None
    org_id: str | None = None

class CanvasUpdate(BaseModel):
    name: str | None = None
    template: CanvasTemplateEnum | None = None
    data: CanvasData | None = None
    visibility: CanvasVisibility | None = None
    group_id: str | None = None
    org_id: str | None = None


class StoredCanvas(CanvasSubmission):
    id: str
    created_at: CoercedUTCDatetime


##### User Models #####
class UserSubmission(BaseModel):
    first_name: str
    last_name: str
    email: LowercaseEmail
    password: str


class StoredUser(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: LowercaseEmail


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
    name: str | None = None  # Because this is the only attribute, it can't be none...


##### Group Models #####
class GroupSubmission(BaseModel):
    name: str
    org_id: str

class StoredGroup(GroupSubmission):
    id: str
    created_at: CoercedUTCDatetime

class GroupUpdate(BaseModel):
    name: str | None = None
    org_id: str | None = None

class GroupMembershipSubmission(BaseModel):
    user_id: str
    role: UserRoleEnum


##### Login Models #####
class LoginRequest(BaseModel):
    email: EmailStr
    password: str