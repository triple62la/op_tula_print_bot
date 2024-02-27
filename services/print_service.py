import asyncio
from typing import TypeVar, Literal, Tuple
from enum import Enum


kyocera = "kyocera"
portrait = "portrait"
landscape = "landscape"

orientation_num_mapper = {portrait: 3, landscape: 4}


class PrintSettings:
    def __init__(self, printer_name: str, copies: int, pages: list[int] | None,
                 orientation: str | None) -> None:
        self.printer_name = printer_name
        self.copies = copies or 1
        self.pages = pages or None
        self.orientation = orientation or None

    def __str__(self) -> str:
        return f"""
        Принтер: {self.printer_name}
        Кол-во копий: {self.copies}
        Номера страниц: {self.pages or 'Все'}
        Ориентация: {self.orientation or "как в документе"}
        """

    def mount_to_string(self) -> str:
        pages = f" -P {', '.join(map(str, self.pages))}" if self.pages is not None else ""
        orientation = f" -o orientation-requested={orientation_num_mapper.get(self.orientation)}" \
            if self.orientation is not None else ""
        return f" -d {self.printer_name} -n {self.copies}{pages}{orientation}"


class DefaultPrintSettings(PrintSettings):
    def __init__(self) -> None:
        super().__init__(kyocera, 1, None, None)


class PrintTask:
    def __init__(self, print_settings: PrintSettings | None = None) -> None:
        self.print_settings = print_settings or DefaultPrintSettings()

    async def exec(self, file_path: str) -> Tuple[str, str]:
        cmd = rf'lp{self.print_settings.mount_to_string()} {file_path}'
        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        return stdout.decode(), stderr.decode()


if __name__ == "__main__":
    def_print_settings = DefaultPrintSettings()
    print(def_print_settings)
