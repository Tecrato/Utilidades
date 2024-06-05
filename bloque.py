import pygame as pag
from pygame import Vector2

from .Animaciones import Curva_de_Bezier, Second_Order_Dinamics, Simple_acceleration
from .obj_Base import Base

class Bloque(Base):
    def __init__(self,pos,size,dire:str='center') -> None:
        super().__init__(pos,dire)

        self.surf = pag.Surface(size)
        self.surf.fill((255, 0, 128))
        self.surf.set_colorkey((255, 0, 128))

        self.list_objs = []
        self.list_to_draw = []
        self.list_to_click = []

    def add(self,clase, relative_pos, *, drawing=True, clicking=False):
        """
        ## relative_pos examples:
         - (200,200)
         - (200,200*2)
         - (200*.01,200)
         - pag.Vector2(200,200)
         - pag.Vector2(self.rect.size)*.4
         - (self.rect.w*.1,self.rect.h*.4)
        """
        self.list_objs.append({"GUI":clase,"pos":relative_pos})
        if drawing:
            self.list_to_draw.append(self.list_objs[-1]["GUI"])
        if clicking:
            self.list_to_click.append(self.list_objs[-1]["GUI"])
        self.list_objs[-1]["GUI"].pos = eval(f"{self.list_objs[-1]["pos"]}")

    def draw(self,surface: pag.Surface):
        self.surf.fill((255, 0, 128))
        for x in self.list_to_draw:
            x.draw(self.surf)
        surface.blit(self.surf,self.rect)

    def update(self, pos=None):
        return super().update(pos)