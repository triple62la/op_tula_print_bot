import os
import aiofiles


async def write_file(file_path: str, file_data: bytes) -> None:
    if not os.path.exists(os.getcwd() + "/downloads"):
        os.mkdir(os.getcwd() + "/downloads")
    async with aiofiles.open(file_path, "wb") as empty_file:
        await empty_file.write(file_data)


def delete_file(file_path: str) -> None:
    os.remove(file_path)
