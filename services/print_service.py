import asyncio
import os
from typing import TypeVar, Literal, Tuple
from enum import StrEnum, IntEnum


class OrientationEnum(IntEnum):
    PORTRAIT = 3
    LANDSCAPE = 4
    DEFAULT = 0


class PrinterNamesEnum(StrEnum):
    KYOCERA = "kyocera"
    HP = "hp"
    RICOH = "ricoh"


Orientation = Literal["portrait", "landscape", "default"]


class PrintSettings:
    def __init__(self, printer_name: PrinterNamesEnum, copies: int, pages: list[int],
                 orientation: OrientationEnum | int) -> None:
        self.printer_name = printer_name
        self.copies = copies or 1
        self.pages = pages
        self.orientation = self.init_orientation(orientation)

    def __str__(self) -> str:
        orientation = self.orientation if self.orientation is not OrientationEnum.DEFAULT else "как в документе"
        return f"""
        Принтер: {self.printer_name}
        Кол-во копий: {self.copies}
        Номера страниц: {self.pages or 'Все'}
        Ориентация: {orientation}
        """

    @staticmethod
    def init_orientation(orientation) -> OrientationEnum:

        if not isinstance(orientation, OrientationEnum):
            for item in OrientationEnum:
                if item.value == orientation:
                    return item
        return orientation

    def mount_to_string(self) -> str:
        pages = f" -P {', '.join(map(str, self.pages))}" if self.pages else ""
        orientation = f" -o orientation-requested={self.orientation.value}" \
            if self.orientation is not OrientationEnum.DEFAULT else ""
        return f" -d {self.printer_name} -n {self.copies}{pages}{orientation}"


class DefaultPrintSettings(PrintSettings):
    def __init__(self) -> None:
        super().__init__(PrinterNamesEnum.KYOCERA, 1, [], OrientationEnum.DEFAULT)


async def exec_task(print_settings: PrintSettings, file_path: str) -> Tuple[str, str]:
    cmd = rf'lp{print_settings.mount_to_string()} {file_path}'
    if os.name == "nt":
        print(cmd)
        return "", ""
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    return stdout.decode(), stderr.decode()


if __name__ == "__main__":
    def_print_settings = PrintSettings(PrinterNamesEnum.KYOCERA, copies=2, pages=[],
                                       orientation=OrientationEnum.DEFAULT)
