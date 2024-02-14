from numpy import pi
from math import comb

from pygame.math import Vector2


def calculate_pos(k1,k2,k3,y,t,x,xd,yd) -> list:
        k2_stable = max(k2,t*t/2 + t*k1/2, t*k1)

        y = y + t * yd
        yd = yd + t * (x + k3*xd - y - k1*yd) / k2_stable
        return [y,yd]


class Second_Order_Dinamics:
    def __init__(self, T, f, z, r, coord:list) -> None:

        self.k1 = z/ (pi*f)
        self.k2 = 1/ ((2*pi*f)**2)
        self.k3 = r * z / (2*pi*f)

        self.__T = 1/T

        self.xp = Vector2(coord)
        self.y = Vector2(coord)
        self.yd = Vector2(coord)

    def update(self, x, xd = None) -> list:
        x = Vector2(x)
        xd = Vector2(xd) if xd != None else None

        if xd == None:
            xd = (x-self.xp) / self.__T
            self.xp = x
        
        result = calculate_pos(self.k1,self.k2,self.k3,self.y,self.__T,x,xd, self.yd)

        self.y = result[0]
        self.yd = result[1]

        return self.y
        


class Curva_de_Bezier:
    def __init__(self, timer, points, extra_time: int = 1) -> None:
        self.__T = 0
        self.timer = timer
        self.extra_time = extra_time
        self.points = [Vector2(ag) for ag in points]
        if len(self.points) < 2:
            raise 'Debes dar 2 puntos o mas para logar la animacion deseada (Cubic Bezier)'

    def move(self, points) -> None:
        self.points = [Vector2(ag) for ag in points]

    def set(self,progress:float):
        ' - Define en que % de la animacion estara'
        self.__T = progress

    def update(self) -> bool:
        self.__T += 1/self.timer
        if self.__T > self.extra_time:
            return True
        result = Vector2([0,0])
        for i,p in enumerate(self.points):
            coeff = comb(len(self.points)-1,i) * self.__T**i * (1-self.__T)**(len(self.points)-1-i)
            result += coeff * p
        return list(result)
