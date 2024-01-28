import math

def Hipotenuza(vector1, vector2) -> int:
    vector1 = Vector2(*vector1)
    vector2 = Vector2(*vector2)
    return math.dist(vector1,vector2)

def Angulo(vector1, vector2) -> float:
    x = vector2[0] - vector1[0]
    y = vector2[1] - vector1[1]
    return math.atan2(y,x) * (180.0 / math.pi)

class Vector2:
    def __init__(self,x:float,y:float) -> None:
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return [self.x,self.y]
    def __str__(self) -> str:
        return f'x:{self.x} - y:{self.y}'
    def __getitem__(self,index) -> list:
        return [self.x,self.y][index] #self.x if index == 0 else self.y
    def __setitem__(self,index,value) -> None:
        if index == 0:
            self.x = float(value)
        elif index == 1:
            self.y = float(value)

    def __add__(self,other) -> list:
        return [self.x+other[0],self.y+other[1]]
        # self.x+=other[0]
        # self.y+=other[1]
        # return self
    def __radd__(self,other) -> list:
        return [self.x+other[0],self.y+other[1]]
    def __sub__(self,other) -> list:
        return [self.x-other[0],self.y-other[1]]
    def __rsub__(self,other) -> list:
        return [self.x-other[0],self.y-other[1]]
    def __mul__(self,other) -> list:
        return [self.x*other[0],self.y*other[1]]
    def __rmul__(self,other) -> list:
        return [self.x*other[0],self.y*other[1]]
    def __truediv__(self,other) -> list:
        return [self.x/other[0],self.y/other[1]]
    def __pow__(self,other) -> list:
        return [self.x**other[0],self.y**other[1]]
