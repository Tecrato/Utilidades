import os
import sys
import datetime
import traceback
import colorama
from typing import Union, Self, Any
from pathlib import Path
from threading import Lock

StrOrPath = Union[str, Path]
print_lock = Lock()
priority_txt = {0:'Debug', 1:'Info', 2:'Warning', 3:'Error', 4:'Critical'}
color_priority = {0:colorama.Fore.BLUE, 1:colorama.Fore.GREEN, 2:colorama.Fore.YELLOW, 3:colorama.Fore.RED, 4:colorama.Fore.MAGENTA}

class Logger:
    """
    Logger
        - name: Nombre del programa
        - path: Ruta de la carpeta donde se guardarán los logs
    """
    def __init__(self, name: str, path: StrOrPath) -> None:
        self.name = name
        self.path = Path(path)
        fecha = datetime.datetime.now()
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        self.alias = f'{name} {fecha.strftime("%d-%m-%y")}.log'
        self.path.joinpath(self.alias).touch(exist_ok=True)
        self.logger = open(self.path / self.alias, 'r+')
        self.logger.read()

    def write(self, text) -> None:
        self.logger.write(str(text)+'\n')
    
    def open_folder(self):
        os.startfile(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.logger.close()
    
    def __del__(self) -> None:
        self.logger.close()
    
    def __close__(self) -> None:
        self.logger.close()

    def __enter__(self) -> Self:
        return self

    def __str__(self) -> str:
        return f'Logger: {self.name}'

    def __repr__(self) -> str:
        return f'Logger: {self.name}'

    def __call__(self, text):
        self.logger.write('{}\n'.format(text))


def debug_print(text: Any, priority: int = 0):
    """
    priority:
        0: Debug
        1: Info
        2: Warning
        3: Error
        4: Critical
    """
    if not 0 <= priority <= 4:
        raise ValueError(f'Invalid priority: {priority}, valid priorities between 0 and 4')
    print_lock.acquire()
    # va a mostrar tambien el nombre del archivo entre parentesis

    file = sys._getframe(1).f_code.co_filename.split('\\')[-1]
    print(f'{color_priority[priority]}[{priority_txt[priority]}] ({file}) Line {sys._getframe(1).f_lineno} -> <{type(text).__name__}>{str(text)}{colorama.Style.RESET_ALL}')
    if traceback.extract_stack() and priority >= 2:
        traceback.print_exc()
    print_lock.release()