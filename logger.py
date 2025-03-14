import datetime, os, sys
from typing import Union, Self, Any
from pathlib import Path
import colorama

StrOrPath = Union[str, Path]

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
    priority_txt = ['Debug', 'Info', 'Warning', 'Error', 'Critical'][priority]
    color_priority = [colorama.Fore.BLUE, colorama.Fore.GREEN, colorama.Fore.YELLOW, colorama.Fore.RED, colorama.Fore.MAGENTA]
    # va a mostrar tambien el nombre del archivo entre parentesis
    file = sys._getframe(1).f_code.co_filename.split('\\')[-1]
    print(f'{color_priority[priority]}[{priority_txt}] ({file}) Line {sys._getframe(1).f_lineno} -> <{type(text).__name__}>{text}{colorama.Style.RESET_ALL}')