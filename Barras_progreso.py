from typing import Tuple
import pygame as pag
from pygame.surface import Surface

class Barra_de_progreso:
    def __init__(self, pos: Tuple[int,int], lenght: int, orientacion = 'vertical') -> None:
        self.lenght = lenght
        self.pos = pos
        self.orientacion = orientacion
        if orientacion == 'vertical':
            self.rect = pag.rect.Rect(0, 0, 10, lenght/2)
            self.rect2 = pag.rect.Rect(0, 0, 10, lenght)
            self.rect.bottomleft = pos
            self.rect2.bottomleft = pos
            self.volumen = float(self.rect.height / self.lenght)
        elif orientacion == 'horizontal':
            self.rect = pag.rect.Rect(0, 0, lenght/2, 10)
            self.rect2 = pag.rect.Rect(0, 0, lenght, 10)
            self.rect.topleft = pos
            self.rect2.topleft = pos
            self.volumen = float(self.rect.w / self.lenght)

    def pulsando(self) -> None:
        g,k = pag.mouse.get_pos()
        if self.orientacion == 'vertical':
            if self.rect2.bottom - k > self.lenght:
                self.rect.height = self.lenght
            elif self.rect2.bottom - k < 0:
                self.rect.height = 0
            else:
                self.rect.height = self.rect2.bottom - k
            self.rect.bottom = self.pos[1]
            self.volumen = float(self.rect.height / self.lenght)
        elif self.orientacion == 'horizontal':
            if self.rect2.left + g > self.lenght:
                self.rect.w = self.lenght
            elif self.rect2.left + g < 0:
                self.rect.w = 0
            else:
                self.rect.w = self.rect2.bottom - g
            self.volumen = float(self.rect.w / self.lenght)
    
    def set_volumen(self, volumen) -> None:
        self.volumen = volumen
        if self.orientacion == 'vertical':
            self.rect.height = self.lenght*volumen
            self.rect.bottom = self.pos[1]
        elif self.orientacion == 'horizontal':
            self.rect.w = self.lenght*volumen
        pag.mixer_music.set_volume(volumen)

    def draw(self,surface) -> None:
        pag.draw.rect(surface, 'lightblue', self.rect2, width=2)
        pag.draw.rect(surface, 'green', self.rect)

    def move(self, pos) -> None:
        self.pos = pos
        if self.orientacion == 'vertical':
            self.rect.bottomleft = pos
            self.rect2.bottomleft = pos
        elif self.orientacion == 'horizontal':
            self.rect.topleft = pos
            self.rect2.topleft = pos