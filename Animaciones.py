from numpy import pi, array as np_array, arange
from math import comb


class Second_Order_Dinamics:
    def __init__(self, T, f, z, r, coord:list) -> None:

        self.k1 = z/ (pi*f)
        self.k2 = 1/ ((2*pi*f)**2)
        self.k3 = r * z / (2*pi*f)

        self.__T = 1/T

        self.profundidad = 2
        self.xp = np_array(coord)
        self.y = np_array(coord)
        self.yd = np_array(arange(len(coord)))
    
    def update(self, x, xd = None) -> list:
        x = np_array(x)
        xd = np_array(xd) if xd != None else None

        if xd == None:
            xd = (x-self.xp) / self.__T
            self.xp = x

        k2_stable = max(self.k2,self.__T*self.__T/2 + self.__T*self.k1/2, self.__T*self.k1)

        self.y = self.y + self.__T * self.yd
        self.yd = self.yd + self.__T * (x + self.k3*xd - self.y - self.k1*self.yd) / k2_stable
        return [self.y[0],self.y[1]]

class Curva_de_Bezier:
    def __init__(self, timer, points, extra_time: int = 1) -> None:
        self.__T = 0
        self.timer = timer
        self.extra_time = extra_time
        self.points = [np_array(ag) for ag in points]
        if len(self.points) < 2:
            raise 'Debes dar 2 puntos o mas para logar la animacion deseada (Cubic Bezier)'

    def move(self, points) -> None:
        self.points = [np_array(ag) for ag in points]

    def set(self,progress:float):
        ''' - Define en que % de la animacion estara'''
        self.__T = progress

    def update(self,) -> bool:
        self.__T += 1/self.timer
        if self.__T > self.extra_time:
            return True
        result = np_array([0,0],dtype='float64')
        for i,p in enumerate(self.points):
            coeff = comb(len(self.points)-1,i) * self.__T**i * (1-self.__T)**(len(self.points)-1-i)
            result += coeff * p
        return list(result)
