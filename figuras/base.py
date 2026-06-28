from typing import List, Tuple
from ..maths import Vector2

class BasePolygon:
    """Clase base optimizada para polígonos con aceleración espacial."""
    def __init__(self,
                 pos: Tuple[float, float],
                 radio: float,
                 angle: float):
        self.__pos = Vector2(pos)
        self.__radio = radio
        self.__angle = angle
        self.figura: List[Tuple[float, float]] = []
        self.rect: Tuple[float, float, float, float] = (0, 0, 0, 0)
        self.use_mouse_wheel = False

    # ==================== PROPIEDADES OPTIMIZADAS ====================
    @property
    def pos(self) -> Vector2:
        return self.__pos
    @pos.setter
    def pos(self, value: Tuple[float, float]):
        if self.__pos != value:
            self.__pos = Vector2(value)
            self.generate()
            self.update_rect()

    @property
    def radio(self) -> float:
        return self.__radio
    @radio.setter
    def radio(self, value: float):
        if self.__radio != value:
            self.__radio = value
            self.generate()
            self.update_rect()

    @property
    def angle(self) -> float:
        return self.__angle
    @angle.setter
    def angle(self, value: float):
        if self.__angle != value:
            self.__angle = float(value)
            self.generate()
    @property
    def height(self) -> float:
        return self.rect[3]-self.rect[1]

    def rotate(self, angle: float):
        self.angle += angle
        
    
    def update_rect(self):
        """Actualiza el AABB (Axis-Aligned Bounding Box) del polígono"""
        if not self.figura:
            self.rect = (0, 0, 0, 0)
            return
            
        min_x = min(p[0] for p in self.figura)
        max_x = max(p[0] for p in self.figura)
        min_y = min(p[1] for p in self.figura)
        max_y = max(p[1] for p in self.figura)
        self.rect = (min_x, min_y, max_x, max_y)


    @property
    def x(self) -> float:
        return self.pos.x
    @x.setter
    def x(self, value: float):
        self.pos.x = value

    @property
    def y(self) -> float:
        return self.pos.y
    @y.setter
    def y(self, value: float):
        self.pos.y = value
    