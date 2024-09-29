from math import comb, pi
from array import array

from typing import Callable

def arrays_operation(arr1, arr2, operation: Callable):
    arr1 = list(arr1) if type(arr1) in [list,tuple,array] else [arr1]
    arr2 = list(arr2) if type(arr2) in [list,tuple,array] else [arr2]
    arr1 = array('f',arr1) if len(arr1) >= len(arr2) else array('f',list(arr1) + [arr1[0]]*(len(arr2)-len(arr1)))
    arr2 = array('f',arr2) if len(arr2) >= len(arr1) else array('f',list(arr2) + [arr2[0]]*(len(arr1)-len(arr2)))
    # return [operation(x, y) for x, y in zip(arr1, arr2)]
    return operation(arr1, arr2)
    
    

def sumar_arrays(arr1, arr2):
    return [x + y for x, y in zip(arr1, arr2)]
def restar_arrays(arr1, arr2):
    return [x - y for x, y in zip(arr1, arr2)]
def multiplicar_arrays(arr1, arr2):
    return [x * y for x, y in zip(arr1, arr2)]
def divide_arrays(arr1, arr2):
    return [x / y for x, y in zip(arr1, arr2)]

class Simple_acceleration:
    def __init__(self,vel, dir,pos) -> None:
        self.vel: float = vel
        self.dir: array = array('f',dir)
        self.pos = array('f',pos)
    def update(self,dt=1) -> array:
        self.pos[0] += self.dir[0]*self.vel*dt
        self.pos[1] += self.dir[1]*self.vel*dt
        return self.pos
    def follow(self,pos,dt=1) -> array[float]:
        el_max = max(self.pos[0]-pos[0],self.pos[1]-pos[1])
        self.dir = (self.pos[0] - pos[0]) - (self.pos[1] - pos[1]) / el_max
        self.pos[0] += self.dir[0]*self.vel*dt
        self.pos[1] += self.dir[1]*self.vel*dt

        return self.pos


class Curva_de_Bezier:
    def __init__(self, timer, points, extra_time: int = 1) -> None:
        self.__T = 0
        self.timer = timer
        self.extra_time = extra_time
        self.points = [array('f',ag) for ag in points]
        if len(self.points) < 2:
            raise 'Debes dar 2 puntos o mas para logar la animacion deseada (Cubic Bezier)'

    def move(self, points) -> None:
        self.points = [array('f',ag) for ag in points]

    def set(self,progress:float) -> None:
        ' - Define en que % de la animacion estara'
        self.__T = progress

    def update(self,dt=1) -> array:
        self.__T += (1/self.timer) * dt
        if self.__T > self.extra_time:
            return True
        result = array('f',[0,0])
        for i,p in enumerate(self.points):
            coeff = comb(len(self.points)-1,i) * self.__T**i * (1-self.__T)**(len(self.points)-1-i)
            result[0] += coeff * p[0]
            result[1] += coeff * p[1]
        return result


class Second_Order_Dinamics:
    def __init__(self, T, f, z, r, coord:list|tuple) -> None:

        self.k1 = z/ (pi*f)
        self.k2 = 1/ ((2*pi*f)**2)
        self.k3 = r * z / (2*pi*f)

        self.__T = 1/T

        self.k2_stable = max(self.k2,self.__T*self.__T/2 + self.__T*self.k1/2, self.__T*self.k1)

        self.xp = array('f',coord)
        self.y = array('f',coord)
        self.yd = array('f',[0,0])

    def update(self, x, xd = None, dt=1) -> array:
        x = array('f',x)

        if xd is None:
            xd = arrays_operation(arrays_operation(x, self.xp, restar_arrays), self.__T, divide_arrays)
            self.xp = x
        else:
            xd = array('f',xd)

        self.y = sumar_arrays(self.y, multiplicar_arrays([self.__T,self.__T], self.yd))
        a = arrays_operation(self.k3, xd, multiplicar_arrays)
        b = arrays_operation(x, a, sumar_arrays)
        c = arrays_operation(b,self.y, restar_arrays)
        d = arrays_operation(self.k1, self.yd, multiplicar_arrays)
        e = arrays_operation(c, d, restar_arrays)
        self.yd = sumar_arrays(self.yd, arrays_operation(arrays_operation(self.__T, e,multiplicar_arrays),self.__T, divide_arrays))
        return self.y
