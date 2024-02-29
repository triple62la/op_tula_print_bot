import sqlalchemy.engine
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import Insert
from services.database.models import Tasks, engine
from services.print_service import OrientationEnum, PrinterNamesEnum


async def db_create_task(uuid: str, user_id: int, chat_id: int, printer_name: PrinterNamesEnum, copies: int,
                         pages: list[int],
                         orientation: OrientationEnum, file_path: str
                         ) -> sqlalchemy.engine.Result:
    pages = ", ".join(map(str, pages))
    async with engine.connect() as conn:
        result = await conn.execute(Insert(Tasks), [{"uuid": uuid,
                                                     "user_id": user_id,
                                                     "chat_id": chat_id,
                                                     "printer_name": printer_name.value,
                                                     "copies": copies,
                                                     "pages": pages,
                                                     "orientation": orientation.value,
                                                     "file_path": file_path
                                                     }]
                                    )
        await conn.commit()
        return result


async def db_get_task_by_id(task_uuid):
    async with engine.connect() as conn:
        result = await conn.execute(select(Tasks).where(Tasks.uuid==task_uuid))
        return result.scalar_one_or_none()

