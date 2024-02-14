from typing import Iterable
import math

def Hipotenuza(vector1, vector2) -> int:
    vector1 = Vector2(*vector1)
    vector2 = Vector2(*vector2)
    return math.dist(vector1,vector2)

def Angulo(vector1, vector2) -> float:
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    angulo = math.atan2(y,x) * (180.0 / math.pi)
    return angulo if angulo > 0 else 180 + (180+angulo)

class Vector2:
    def __init__(self,*args) -> None:
        if len(args) == 1:
            self.x,self.y = args[0]
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
    
    def __repr__(self) -> str:
        return [self.x,self.y]
    def __str__(self) -> str:
        return f'x:{self.x} - y:{self.y}'
    def __len__(self) -> str:
        return 2
    def __getitem__(self,index) -> list:
        return [self.x,self.y][index]
    def __setitem__(self,index,value) -> None:
        if index == 0:
            self.x = float(value)
        elif index == 1:
            self.y = float(value)

    def __add__(self,other) -> list:
        return [self.x+other[0],self.y+other[1]]
    def __radd__(self,other) -> list:
        return [self.x+other[0],self.y+other[1]]
    def __sub__(self,other) -> list:
        return [self.x-other[0],self.y-other[1]] if isinstance(other,Iterable) else [self.x-other,self.y-other]
    def __rsub__(self,other) -> list:
        return [self.x-other[0],self.y-other[1]] if isinstance(other,Iterable) else [self.x-other,self.y-other]
    def __mul__(self,other) -> list:
        return [self.x*other[0],self.y*other[1]]
    def __rmul__(self,other) -> list:
        return [self.x*other[0],self.y*other[1]]
    def __truediv__(self,other) -> list:
        return [self.x/other[0],self.y/other[1]]
    def __pow__(self,other) -> list:
        return [self.x**other[0],self.y**other[1]]
