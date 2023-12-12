import pygame as pag, math
from numpy import pi

class Second_Order_Dinamics:
    def __init__(self, T, f, z, r, coord:list) -> None:

        self.k1 = z/ (pi*f)
        self.k2 = 1/ ((2*pi*f)**2)
        self.k3 = r * z / (2*pi*f)

        self.T = T

        if len(coord) == 2 :
            self.profundidad = 2
            self.xp = pag.math.Vector2(coord)
            self.y = pag.math.Vector2(coord)
            self.yd = pag.math.Vector2()
        elif len(coord) == 3 :
            self.profundidad = 3
            self.xp = pag.math.Vector3(coord)
            self.y = pag.math.Vector3(coord)
            self.yd = pag.math.Vector3()
    
    def update(self, x, xd = None) -> list:
        if self.profundidad == 2:
            x = pag.math.Vector2(x)
            xd = pag.math.Vector2(xd) if xd != None else None
        elif self.profundidad == 3:
            x = pag.math.Vector3(x)
            xd = pag.math.Vector3(xd) if xd != None else None

        if xd == None:
            xd = (x-self.xp) / self.T
            self.xp = x

        k2_stable = max(self.k2,self.T*self.T/2 + self.T*self.k1/2, self.T*self.k1)

        self.y = self.y + self.T * self.yd
        self.yd = self.yd + self.T * (x + self.k3*xd - self.y - self.k1*self.yd) / k2_stable
        return self.y


# class Curva_de_Bezier:
#     def __init__(self, timer, points, extra_time: int = 1) -> None:
#         self.T = 0
#         self.timer = timer
#         self.extra_time = extra_time
#         self.points = [ag for ag in points]
#         if len(self.points) < 2:
#             raise 'Debes dar 2 puntos o mas para logar la animacion deseada (Cubic Bezier)'
#         if len(self.points) > 1:
#             self.a = pag.math.Vector2(self.points[0])
#             self.b = pag.math.Vector2(self.points[1])
#         if len(self.points) > 2:
#             self.c = pag.math.Vector2(self.points[2])
#         if len(self.points) > 3:
#             self.d = pag.math.Vector2(self.points[3])
#         if len(self.points) > 4:
#             self.e = pag.math.Vector2(self.points[4])
    
#     def move(self, points) -> None:
#         self.points = [ag for ag in points]
#         if len(self.points) > 0:
#             self.a = pag.math.Vector2(self.points[0])
#         if len(self.points) > 1:
#             self.b = pag.math.Vector2(self.points[1])
#         if len(self.points) > 2:
#             self.c = pag.math.Vector2(self.points[2])
#         if len(self.points) > 3:
#             self.d = pag.math.Vector2(self.points[3])
#         if len(self.points) > 4:
#             self.e = pag.math.Vector2(self.points[4])

#     def update(self) -> bool:
#         self.T += 1/self.timer
#         if self.T > self.extra_time:
#             return True
#         if len(self.points) == 2:
#             p = (1-self.T)*self.a + (self.T*self.b)
#             return pag.math.Vector2(p)
#         elif len(self.points) == 3:
#             p1 = (1-self.T)*self.a + (self.T*self.b)
#             p2 = (1-self.T)*self.b + (self.T*self.c)
#             p3 = (1-self.T)*p1 + (self.T*p2)
#             return pag.math.Vector2(p3)
#         elif len(self.points) == 4:
#             p1 = (1-self.T)*self.a + (self.T*self.b)
#             p2 = (1-self.T)*self.b + (self.T*self.c)
#             p3 = (1-self.T)*self.c + (self.T*self.d)
#             pu1 = (1-self.T)*p1 + (self.T*p2)
#             pu2 = (1-self.T)*p2 + (self.T*p3)
#             pf = (1-self.T)*pu1 + (self.T*pu2)
#             return pag.math.Vector2(pf)
#         elif len(self.points) == 5:
#             p1 = (1-self.T)*self.a + (self.T*self.b)
#             p2 = (1-self.T)*self.b + (self.T*self.c)
#             p3 = (1-self.T)*self.c + (self.T*self.d)
#             p4 = (1-self.T)*self.d + (self.T*self.e)
#             pu1 = (1-self.T)*p1 + (self.T*p2)
#             pu2 = (1-self.T)*p2 + (self.T*p3)
#             pu3 = (1-self.T)*p3 + (self.T*p4)
#             pun1 = (1-self.T)*pu1 + (self.T*pu2)
#             pun2 = (1-self.T)*pu2 + (self.T*pu3)
#             pf = (1-self.T)*pun1 + (self.T*pun2)
#             return pag.math.Vector2(pf)
class Curva_de_Bezier:
    def __init__(self, timer, points, extra_time: int = 1) -> None:
        self.T = 0
        self.timer = timer
        self.extra_time = extra_time
        self.points = [pag.math.Vector2(ag) for ag in points]
        if len(self.points) < 2:
            raise 'Debes dar 2 puntos o mas para logar la animacion deseada (Cubic Bezier)'

    def move(self, points) -> None:
        self.points = [pag.math.Vector2(ag) for ag in points]

    def update(self) -> bool:
        self.T += 1/self.timer
        if self.T > self.extra_time:
            return True
        result = pag.math.Vector2(0,0)
        for i,p in enumerate(self.points):
            coeff = math.comb(len(self.points)-1,i) * self.T**i * (1-self.T)**(len(self.points)-1-i)
            result += coeff * p
        return result
