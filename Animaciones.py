from math import comb, pi
from array import array
from .maths import arrays_operation, Vector2

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
    def __init__(self, T, f, z, r, coord:list|tuple|Vector2) -> None:

        self.k1 = z/ (pi*f)
        self.k2 = 1/ ((2*pi*f)**2)
        self.k3 = r * z / (2*pi*f)

        self.__T = 1/T

        self.k2_stable = max(self.k2,self.__T*self.__T/2 + self.__T*self.k1/2, self.__T*self.k1)

        self.xp = Vector2(coord)
        self.y = Vector2(coord)
        self.yd = Vector2(0,0)

    def update(self, x, xd = None, dt=1) -> Vector2:
        x = Vector2(x)

        if xd is None:
            xd = (x-self.xp) / self.__T
            self.xp = x
        else:
            xd = Vector2(xd)

        self.y = self.y + self.__T * (self.yd * dt)
        self.yd = self.yd + self.__T * (x + self.k3*xd - self.y - self.k1*self.yd) / self.k2_stable
        return self.y
