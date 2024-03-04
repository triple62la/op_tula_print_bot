import datetime
from enum import StrEnum
from typing import Optional
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



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
    reply_id: Mapped[int]
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    printer_name: Mapped[str]
    copies: Mapped[int] = mapped_column(default=1)
    pages: Mapped[Optional[str]] = mapped_column(nullable=True)
    orientation: Mapped[int]
    file_path: Mapped[str]
    status: Mapped[TaskStatusEnum] = mapped_column(default=TaskStatusEnum.WAITING)

# class SavedPrintSettings(Base):
#     __tablename__ = "b"
#     user_id: Mapped[int]
#     printer_name: Mapped[str]
#     copies: Mapped[int] = mapped_column(default=1)
#     pages: Mapped[Optional[str]] = mapped_column(nullable=False)
#     data: Mapped[str]


# async def async_main() -> None:
#
#
#     # async_sessionmaker: a factory for new AsyncSession objects.
#     # expire_on_commit - don't expire objects after transaction commit
#     async_session = async_sessionmaker(engine, expire_on_commit=False)
#
#
#
#     await insert_objects(async_session)
#     await select_and_update_objects(async_session)
#
#     # for AsyncEngine created in function scope, close and
#     # clean-up pooled connections
#     await engine.dispose()


if __name__ == '__main__':
    pass
