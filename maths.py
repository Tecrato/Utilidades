import math
from typing import Callable
from array import array

from .optimize import memosize

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

def line_intersect(p1,p2,p3,p4):
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
        if Hipotenuza(center,r) < max_radio:
            intersections.append(r)
    return sorted(intersections, key=lambda x: Hipotenuza(line[0],x))


def arrays_operation(arr1, arr2, operation: str = "sumar"):
    if not len(arr1) or not len(arr2):
        raise ValueError("Los arreglos deben tener al menos un elemento")
    arr1 = list(arr1) if type(arr1) in [list,tuple,array] else [arr1]
    arr2 = list(arr2) if type(arr2) in [list,tuple,array] else [arr2]
    arr1 = array('f',arr1) if len(arr1) >= len(arr2) else array('f',list(arr1) + [arr1[0]]*(len(arr2)-len(arr1)))
    arr2 = array('f',arr2) if len(arr2) >= len(arr1) else array('f',list(arr2) + [arr2[0]]*(len(arr1)-len(arr2)))

    if operation == 'sumar':
        return [x + y for x, y in zip(arr1, arr2)]
    elif operation == 'restar':
        return [x - y for x, y in zip(arr1, arr2)]
    elif operation == 'multiplicar':
        return [x * y for x, y in zip(arr1, arr2)]
    elif operation == 'dividir':
        return [x / y for x, y in zip(arr1, arr2)]
    else:
        return [x + y for x, y in zip(arr1, arr2)]
    

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