import datetime
from typing import Union, Self
from pathlib import Path

StrOrPath = Union[str, Path]

class Logger:
    """
    Logger
        - name: Nombre del logger
        - path: Ruta donde se guardará el log
    """
    def __init__(self, name: str, path: StrOrPath) -> None:
        self.name = name
        self.path = Path(path)
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        self.path.joinpath(f'{name} {datetime.datetime.now().strftime("%d-%m-%y")}.log').touch(exist_ok=True)
        self.logger = open(path / f'{name} {datetime.datetime.now().strftime("%d-%m-%y")}.log', 'r+')
        self.logger.write(f'Logger: {name} iniciado\n')

    def write(self, text) -> None:
        self.logger.write(str(text)+'\n')

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

    def __call__(self, name):
        self.logger.write(f'{name} iniciado\n')