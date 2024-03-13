import sqlalchemy.engine
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.sqlite import Insert
from sqlalchemy.orm import sessionmaker
from services.database.models import Tasks, engine
from services.print_service import OrientationEnum, PrinterNamesEnum
from sqlalchemy.ext.asyncio import AsyncSession

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def db_create_task(uuid: str, user_id: int, chat_id: int, message_id: int, reply_id: int,
                         printer_name: PrinterNamesEnum,
                         copies: int,
                         pages: list[int],
                         orientation: OrientationEnum, file_path: str
                         ) -> sqlalchemy.engine.Result:
    pages = ", ".join(map(str, pages))
    async with engine.connect() as conn:
        result = await conn.execute(Insert(Tasks), [{"uuid": uuid,
                                                     "user_id": user_id,
                                                     "chat_id": chat_id,
                                                     "message_id": message_id,
                                                     "reply_id": reply_id,
                                                     "printer_name": printer_name.value,
                                                     "copies": copies,
                                                     "pages": pages,
                                                     "orientation": orientation.value,
                                                     "file_path": file_path,
                                                     }]
                                    )
        await conn.commit()
        return result


async def db_get_task_by_id(task_uuid):
    async with async_session() as session:
        result = await session.execute(select(Tasks).where(Tasks.uuid == task_uuid))
        return result.scalars().one_or_none()


async def db_remove_task_by_id(task_uuid):
    async with async_session() as session:
        await session.execute(delete(Tasks).where(Tasks.uuid == task_uuid))
        await session.commit()


async def db_set_param_by_id(task_uuid, **params):
    async with async_session() as session:
        await session.execute(update(Tasks).where(Tasks.uuid == task_uuid).values(**params))
        await session.commit()
