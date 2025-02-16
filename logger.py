import datetime, os
from typing import Union, Self
from pathlib import Path

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
        # self.logger.write(f'Logger: {name} iniciado {fecha.strftime("%d-%m-%y %H:%M:%S")} \n')

    def write(self, text) -> None:
        self.logger.write(str(text)+'\n')
    
    def open(self):
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