import math


UNIDADES_BYTES = {
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

def Hipotenuza(vector1, vector2) -> int:
    return math.dist(vector1,vector2)

def Angulo(vector1, vector2) -> float:
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    angulo = math.atan2(y,x) * (180.0 / math.pi)
    return angulo if angulo > 0 else 180 + (180+angulo)

def format_size_bits_to_bytes(size) -> list:
    count = 0
    while size > 1024:
        size /= 1024
        count += 1
    return [count, size]
def format_size_bits_to_bytes_str(size) -> str:
    count = 0
    while size > 1024:
        size /= 1024
        count += 1
    return f"{size:.2f}{UNIDADES_BYTES[count]}"
def convertir_notacion_cientifica(n) -> str:
    s  = str(n)
    return s[0] + '.' + s[1:4] + 'x10^' + str(len(s[1:]))

diccionario = {}

def fibonacci(n):
    '''
    a los 200_000 ya empieza a consumir 2Gb de RAM, asi que lo limite mejor, no quiero lloros.
    '''
    if len(diccionario) > 200_000:
        diccionario.clear()
    if n in diccionario:
        return diccionario[n]
    if n < 2:
        return n
    diccionario[n] = fibonacci(n - 1) + fibonacci(n - 2)
    return diccionario[n]

def pendiente_entre_2_puntos(p1,p2):
    if p1[0] == p2[0]:
        return [0,0]
    b = (p2[1]-p1[1])/(p2[0]-p1[0])
    a = p1[1] - b*p1[0]
    return [a,b]

def line_intersect_con_pendiente(a,c,b,d):
    if a == b:
        return [0,0]
    return [(d-c)/(a-b),(a*d-b*c)/(a-b)]

def line_intersect(p1,p2,p3,p4) -> tuple:
    a1 = p1[1] - p2[1]
    b1 = p1[0] - p2[0]
    c1 = a1*p1[0] - b1*p1[1]
    a2 = p3[1] - p4[1]
    b2 = p3[0] - p4[0]
    c2 = a2*p3[0] - b2*p3[1]
    if a1*b2 - a2*b1 == 0:
        return False
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
        raise ValueError("Debe ingresar al menos 2 puntos")
    suma = [0 for _ in range(len(coordenadas[0]))]
    for x in coordenadas:
        for i in range(len(x)):
            suma[i] += x[i]
    media = [x/len(coordenadas) for x in suma]
    return media


# Integración numérica por el método del trapecio
def integral_de_una_funcion(a, b, func, steps=1000):
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

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

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
