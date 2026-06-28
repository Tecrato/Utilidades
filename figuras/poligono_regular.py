from typing import Tuple
from .base import BasePolygon
from math import sin, cos, radians
class PoligonoRegular(BasePolygon):
    def __init__(self,
                 pos: Tuple[float, float] = (0, 0),
                 lados: int = 4,
                 radio: float = 10,
                 angle: float = 0,):
        super().__init__(pos, radio, angle)
        self.__lados = lados
        self.generate()

    def generate(self):
        step = 360 / self.__lados
        self.figura = [
            (
                self.pos.x + cos(radians(step * i + self.angle)) * self.radio,
                self.pos.y + sin(radians(step * i + self.angle)) * self.radio
            ) for i in range(self.__lados)
        ]
        

    @property
    def lados(self) -> int:
        return self.__lados
    @lados.setter
    def lados(self, value: int):
        if int(value) < 3:
            raise ValueError("El número de lados debe ser mayor o igual a 3")
        if self.__lados != value:
            self.__lados = value
            self.generate()
