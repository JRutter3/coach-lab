from datetime import datetime
from enum import Enum, auto
from typing import Any

import ulid
from api.api_models import CanvasTemplateEnum
from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy import Enum as DBEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class GroupRoleEnum(Enum):
    MEMBER=auto()
    ADMIN=auto()

class CanvasVisibility(Enum):
    PRIVATE=auto()
    GROUP=auto()
    ORG=auto()

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "app_users"
    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=lambda: str(ulid.ulid())
    )
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class Organization(Base):
    __tablename__ = "orgs"
    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=lambda: str(ulid.ulid())
    )
    name: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=lambda: str(ulid.ulid())
    )
    name: Mapped[str] = mapped_column(String(100))
    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(), server_default=func.now())
    __table_args__ = (
        UniqueConstraint("name", "org_id"),
    )


class GroupMembership(Base):
    __tablename__ = "group_membership"
    user_id: Mapped[str] = mapped_column(ForeignKey("app_users.id"), primary_key=True)
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), primary_key=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id"), nullable=False)
    role: Mapped[GroupRoleEnum] = mapped_column(
        DBEnum(GroupRoleEnum), default=GroupRoleEnum.MEMBER
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["group_id", "org_id"],
            ["groups.id", "groups.org_id"],
            name="fk_group_membership_group_org"
        ),
    )
    

class OrgMembership(Base):
    __tablename__ = "org_membership"
    user_id: Mapped[str] = mapped_column(ForeignKey("app_users.id"), primary_key=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id"), primary_key=True)


class CanvasTable(Base):
    __tablename__ = "canvases"
    id: Mapped[str] = mapped_column(
        String(26),
        primary_key=True,
        default=lambda: str(ulid.ulid())
    )
    template: Mapped[CanvasTemplateEnum] = mapped_column(
        DBEnum(CanvasTemplateEnum),
        nullable=False
    )
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    owner_id: Mapped[str] = mapped_column(ForeignKey("app_users.id"), nullable=False)
    visibility: Mapped[CanvasVisibility] = mapped_column(
        DBEnum[CanvasVisibility],
        default=CanvasVisibility.PRIVATE
    )
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), nullable=True)
    org_id: Mapped[str] = mapped_column(ForeignKey("orgs.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime())
    updated_at: Mapped[datetime] = mapped_column(DateTime())

    __table_args__ = (
        CheckConstraint(
            "(visibility = 'private' AND group_id IS NULL AND org_id IS NULL) OR "
            "(visibility = 'group' AND group_id IS NOT NULL) OR "
            "(visibility = 'organization' AND org_id IS NOT NULL)",
            name="check_visibility_constraints"
        ),
    )
