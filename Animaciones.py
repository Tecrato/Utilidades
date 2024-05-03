from numpy import pi, sin, cos, radians
from math import comb
from .optimize import memosize
from .hipotenuza import Angulo_normalized, Angulo
from dataclasses import dataclass

from pygame.math import Vector2

class Simple_acceleration:
    def __init__(self,vel,pos) -> None:
        self.vel: Vector2 = Vector2(vel)
        self.pos = Vector2(pos)
    def update(self,pos,dt=1) -> Vector2:
        angle = Angulo(self.pos, pos)
        self.vel = Vector2(cos(radians(angle)),sin(radians(angle)))
        return self.pos + self.vel
        return (self.pos+Vector2(Angulo_normalized(self.pos,Vector2(pos))*self.vel))


class Second_Order_Dinamics:
    def __init__(self, T, f, z, r, coord:list) -> None:

        self.k1 = z/ (pi*f)
        self.k2 = 1/ ((2*pi*f)**2)
        self.k3 = r * z / (2*pi*f)

        self.__T = 1/T

        self.xp = Vector2(coord)
        self.y = Vector2(coord)
        self.yd = Vector2(0,0)

    def update(self, x, xd = None) -> list:
        x = Vector2(x)
        xd = Vector2(xd) if xd != None else None

        if xd == None:
            xd = (x-self.xp) / self.__T
            self.xp = x
        

        k2_stable = max(self.k2,self.__T*self.__T/2 + self.__T*self.k1/2, self.__T*self.k1)

        self.y = self.y + self.__T * self.yd
        self.yd = self.yd + self.__T * (x + self.k3*xd - self.y - self.k1*self.yd) / k2_stable
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

    def set(self,progress:float) -> None:
        ' - Define en que % de la animacion estara'
        self.__T = progress

    def update(self) -> bool|list[float,float]:
        self.__T += 1/self.timer
        if self.__T > self.extra_time:
            return True
        result = Vector2([0,0])
        for i,p in enumerate(self.points):
            coeff = comb(len(self.points)-1,i) * self.__T**i * (1-self.__T)**(len(self.points)-1-i)
            result += coeff * p
        return list(result)
