from typing import List, Dict, Tuple
from .base import BasePolygon
from math import sin, cos, radians

class PoligonoIrregular(BasePolygon):
    """Polígono irregular con soporte para formas complejas y actualización diferencial."""
    def __init__(self, 
                 puntos: List[Dict[str, float]], 
                 pos: Tuple[float, float] = (0, 0), 
                 radio: float = 20, 
                 angle: float = 0, 
                 cell_size: float = 50.0):
        super().__init__(pos, radio, angle, cell_size)
        self.__puntos = puntos
        self.__generate()

    def __generate(self):
        """Generación vectorizada con transformaciones in situ"""
        self._figure = [
            (
                self._pos[0] + cos(radians(p[0] + self._angle)) * p[1] * self._radio,
                self._pos[1] - sin(radians(p[0] + self._angle)) * p[1] * self._radio
            ) for p in self.__puntos
        ]
        self.update_rect()

    def actualizar_punto(self, index: int, **kwargs):
        """Actualización parcial de un punto con invalidación selectiva"""
        if 'angle' in kwargs or 'radio' in kwargs:
            self.__puntos[index].update(kwargs)
            self.__generate()