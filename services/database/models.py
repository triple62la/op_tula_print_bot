import datetime
from enum import StrEnum
from typing import Optional
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class AllowedUserRoles(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"

class Base(AsyncAttrs, DeclarativeBase):
    pass


engine = create_async_engine(f"sqlite+aiosqlite:///database.db", echo=True)


class TaskStatusEnum(StrEnum):
    WAITING = "WAITING"
    PENDING = "PENDING"


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str]
    user_id: Mapped[int]
    chat_id: Mapped[int]
    message_id: Mapped[int]
    reply_id: Mapped[int]
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    printer_name: Mapped[str]
    copies: Mapped[int] = mapped_column(default=1)
    pages: Mapped[Optional[str]] = mapped_column(nullable=True)
    orientation: Mapped[int]
    file_path: Mapped[str]
    status: Mapped[TaskStatusEnum] = mapped_column(default=TaskStatusEnum.WAITING)



# class AllowedUsers(Base):
#     __tablename__ = "allowed_users"
#
#     id: Mapped[int]
#     first_name: Mapped[str]
#     last_name: Mapped[str]
#     username: Mapped[str]
#     role: Mapped[AllowedUserRoles]
#


if __name__ == '__main__':
    pass
