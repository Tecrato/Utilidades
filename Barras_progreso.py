from typing import Tuple
import pygame as pag

class Barra_de_progreso:
    def __init__(self, pos: Tuple[int,int], size: int, orientacion = 'vertical') -> None:
        self.size = pag.Vector2(size)
        self.pos = pos
        self.orientacion = orientacion
        self.rect = pag.rect.Rect(0, 0, *self.size)
        self.rect2 = pag.rect.Rect(0, 0, *self.size)
        self.volumen = 1.0
        if orientacion == 'vertical':
            self.rect.bottomleft = pos
            self.rect2.bottomleft = pos
        elif orientacion == 'horizontal':
            self.rect.topleft = pos
            self.rect2.topleft = pos

    def pulsando(self) -> None:
        g,k = pag.mouse.get_pos()
        if self.orientacion == 'vertical':
            if self.rect2.bottom - k > self.size.y:
                self.rect.height = self.size.y
            elif self.rect2.bottom - k < 0:
                self.rect.height = 0
            else:
                self.rect.height = self.rect2.bottom - k
            self.rect.bottom = self.pos[1]
            self.volumen = float(self.rect.height / self.size.y)
        elif self.orientacion == 'horizontal':
            if self.rect2.left + g > self.size.x:
                self.rect.w = self.size.x
            elif self.rect2.left + g < 0:
                self.rect.w = 0
            else:
                self.rect.w = self.rect2.bottom - g
            self.volumen = float(self.rect.w / self.size.x)
    
    def set_volumen(self, volumen) -> None:
        self.volumen = volumen
        if self.orientacion == 'vertical':
            self.rect.height = self.size.y*volumen
            self.rect.bottom = self.pos[1]
        elif self.orientacion == 'horizontal':
            self.rect.w = self.size.x*volumen
        pag.mixer_music.set_volume(volumen)

    def draw(self,surface) -> None:
        pag.draw.rect(surface, 'green', self.rect)
        pag.draw.rect(surface, 'darkblue', self.rect2, width=2)

    def move(self, pos) -> None:
        self.pos = pos
        if self.orientacion == 'vertical':
            self.rect.bottomleft = pos
            self.rect2.bottomleft = pos
        elif self.orientacion == 'horizontal':
            self.rect.topleft = pos
            self.rect2.topleft = pos