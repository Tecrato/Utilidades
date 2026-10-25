import os
import sys
import datetime
import traceback
import colorama
from typing import Union, Self, Any, Optional
from pathlib import Path
from threading import Lock


colorama.init(autoreset=True)

StrOrPath = Union[str, Path]
print_lock = Lock()
priority_txt = {
    0:'Debug', 
    1:'Info', 
    2:'Warning', 
    3:'Error', 
    4:'Critical'
}
DEBUG, INFO, WARNING, ERROR, CRITICAL = range(5)
color_priority = {
    0:colorama.Fore.BLUE, 
    1:colorama.Fore.GREEN, 
    2:colorama.Fore.YELLOW, 
    3:colorama.Fore.RED, 
    4:colorama.Fore.MAGENTA
}

class Logger:
    """
    Logger
        - name: Nombre del programa
        - path: Ruta de la carpeta donde se guardarán los logs
    """
    def __init__(self, name: str, path: StrOrPath, printing=False) -> None:
        self.name = name
        self.printing = printing
        self.path = Path(path)
        fecha = datetime.datetime.now()
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        self.alias = f'{name} {fecha.strftime("%d-%m-%y")}.log'
        self.path.joinpath(self.alias).touch(exist_ok=True)
        self.logger = open(self.path / self.alias, 'r+',encoding='utf-8')
        self.logger.read()

    def write(self, text) -> None:
        if self.printing:
            with print_lock:
                print("Añadido a logger:", text)
        self.logger.write(str(text)+'\n')
    
    def open_folder(self):
        os.startfile(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.logger.close()

    def __enter__(self) -> Self:
        return self

    def __str__(self) -> str:
        return f'Logger: {self.name}'

    def __repr__(self) -> str:
        return f'Logger: {self.name}'

    def __call__(self, text):
        self.logger.write('{}\n'.format(text))


def debug_print(*text: Any, priority: int = 0, logger: Optional[Logger] = None) -> None:
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
    with print_lock:
        # va a mostrar tambien el nombre del archivo entre parentesis

        marco = sys._getframe(1)
        fichero = Path(marco.f_code.co_filename).name
        text_file_2_deep = ""
        try :
            text_file_2_deep = f"({Path(sys._getframe(2).f_code.co_filename).name}) {sys._getframe(2).f_lineno} -> "
        except:
            text_file_2_deep = ""
            
        print(f'[{priority_txt[priority]}] {datetime.datetime.now().strftime("%H:%M:%S")} {text_file_2_deep}{color_priority[priority]}({fichero}) ',end="")
        for x in text:
            print(f'{color_priority[priority]}Line {sys._getframe(1).f_lineno} -> <{type(x).__name__}>{str(x)}',end=" ")
        print("\n",end=colorama.Style.RESET_ALL)
        if priority >= 2 and sys.exc_info()[0] is not None:
            traceback.print_exc() 

    
    if logger:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        logger.write(f"[{priority_txt[priority]}] {timestamp} -> {' '.join(str(t) for t in text)}")