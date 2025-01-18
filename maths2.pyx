# distutils: language = c++
# cython: language_level=3, boundscheck=False, wraparound=False, embedsignature=True
import math
from libcpp.math cimport sqrt, atan2, M_PI

from .optimize import memosize

def Hipotenuza(vector1, vector2) -> int:
    return math.dist(vector1,vector2)

cdef Angulo(int vector1[2], int vector2[2]):
    result = atan2(vector2[1] - vector1[1], vector2[0] - vector1[0]) * (180.0 / M_PI)
    return result if result > 0 else 180 + (180+result)

@memosize
def format_size_bits_to_bytes_str(size) -> str:
    count = 0
    while size > 1024:
        size /= 1024
        count += 1
    return f"{size:.2f}{UNIDADES_BYTES[count]}"


UNIDADES_BYTES: dict = {
    0: 'B',
    1: 'KB',
    2: 'MB',
    3: 'GB',
    4: 'TB',
    5: 'PB',
    6: 'EB',
    7: 'ZB',
    8: 'YB'
}

cdef pendiente_entre_2_puntos(int p1[2], int p2[2]):
    if p1[0] == p2[0]:
        return [0,0]
    b = (p2[1]-p1[1])/(p2[0]-p1[0])
    a = p1[1] - b*p1[0]
    return (a,b)

cdef line_intersect_con_pendiente(int a, int c, int b, int d):
    if a == b:
        return (0,0)
    return ((d-c)/(a-b),(a*d-b*c)/(a-b))

cdef line_intersect(int p1[2], int p2[2], int p3[2], int p4[2]):
    if ((p3[1] == p4[1] or p1[0] == p2[0]) and (p1[1] == p2[1] or p3[0] == p4[0])):
        return False
    a1 = p1[1] - p2[1]
    b1 = p1[0] - p2[0]
    c1 = a1*p1[0] - b1*p1[1]
    a2 = p3[1] - p4[1]
    b2 = p3[0] - p4[0]
    c2 = a2*p3[0] - b2*p3[1]
    x = (b2*c1 - b1*c2) / (a1*b2 - a2*b1)
    y = (a2*c1 - a1*c2) / (a1*b2 - a2*b1)
    return (x,y)

def line_to_polygon_intersection(line, polygon, center, max_radio):
    intersections = []
    for i in range(len(polygon)):
        r=line_intersect(*line, polygon[i-1],polygon[i])
        if r and Hipotenuza(center,r) < max_radio:
            intersections.append(r)
    return sorted(intersections, key=lambda x: Hipotenuza(line[0],x))

def media_entre_coordenadas(coordenadas: list[tuple]):
    if not coordenadas:
        raise ValueError("Debe ingresar al menos un punto")
    suma = [0 for _ in range(len(coordenadas[0]))]
    for x in coordenadas:
        for i in range(len(x)):
            suma[i] += x[i]
    media = [x/len(coordenadas) for x in suma]
    return media


# Integración numérica por el método del trapecio
@cython.locals(step_size=float, total_area=float, x1=float, x2=float, y1=float, y2=float)
cdef integral_de_una_funcion(int a, int b, int func(int), int steps=1000):
    step_size = (b - a) / steps
    total_area = 0

    for i in range(steps):
        x1 = a + i * step_size
        x2 = x1 + step_size
        y1 = func(x1)
        y2 = func(x2)
        # Área bajo la curva
        total_area += (y1 + y2) * step_size / 2

    return total_area

    
class Vector2:
    __slots__ = ('x', 'y')
    def __init__(self, x=0, y=0):
        self.x = x if not isinstance(x, (list, tuple)) else x[0]
        self.y = y if not isinstance(x, (list, tuple)) else x[1]

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __rsub__(self, other):
        return Vector2(other.x - self.x,other.y - self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)

    def __rtruediv__(self, other):
        return Vector2(other.x / self.x,other.y / self.y)

    def __repr__(self):
        return f"Vector2({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, item):
        return self.x if item == 0 else self.y
