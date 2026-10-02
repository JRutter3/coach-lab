"""
API Models showing what we expect from the front-end
"""
########################################################################
# NOTE: Pydantic model attribue name MUST match database column names! #
########################################################################

import datetime as dt
from enum import StrEnum, auto
from typing import Annotated, Literal

from pydantic import (
    AwareDatetime,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
)
from pydantic.alias_generators import to_camel

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


class CamelModel(BaseModel):
    model_config=ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )

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

class CanvasSubmission(CamelModel):
    name: str
    template: CanvasTemplateEnum
    data: CanvasData
    visibility: CanvasVisibility
    group_id: str | None = None
    org_id: str | None = None

class CanvasUpdate(CamelModel):
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
class UserSubmission(CamelModel):
    first_name: str
    last_name: str
    email: LowercaseEmail
    password: str


class StoredUser(CamelModel):
    id: str
    first_name: str
    last_name: str
    email: LowercaseEmail


class UserUpdate(CamelModel):
    first_name: str | None = None
    last_name: str | None = None
    email: LowercaseEmail | None = None


##### Organization Models #####
class OrgSubmission(CamelModel):
    name: str


class StoredOrg(OrgSubmission):
    id: str
    created_at: CoercedUTCDatetime


class OrgUpdate(CamelModel):
    name: str | None = None  # Because this is the only attribute, it can't be none...


##### Group Models #####
class GroupSubmission(CamelModel):
    name: str
    org_id: str

class StoredGroup(GroupSubmission):
    id: str
    created_at: CoercedUTCDatetime

class GroupUpdate(CamelModel):
    name: str | None = None
    org_id: str | None = None

class GroupMembershipSubmission(CamelModel):
    user_id: str
    role: UserRoleEnum


##### Login Models #####
class LoginRequest(CamelModel):
    email: EmailStr
    password: str

class UserData(BaseModel):
    id: str
    email: str
    exp: AwareDatetime