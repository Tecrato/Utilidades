from typing import Iterable
import math
from pygame import Vector2

def Hipotenuza(vector1, vector2) -> int:
    vector1 = Vector2(*vector1)
    vector2 = Vector2(*vector2)
    return math.dist(vector1,vector2)

def Angulo(vector1, vector2) -> float:
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    angulo = math.atan2(y,x) * (180.0 / math.pi)
    return angulo if angulo > 0 else 180 + (180+angulo)

def Angulo_normalized(vector1, vector2) -> Vector2:
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    return (Vector2(x,y).normalize() if x != 0 or y != 0 else Vector2(0,0))

Angulo_normalized((0,100),(100,125))