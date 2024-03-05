import pygame as pag, math

from ..text import Create_boton, Create_text
from pygame.math import Vector2



class mini_GUI_admin:
    def __init__(self, limit_rect: pag.Rect) -> None:
        self.__list = []
        self.limit_rect = limit_rect
    
    
    def get_limit_rect(self) -> pag.Rect:
        return self.limit_rect
    
    def add(self,mini_GUI,func=None):
        self.__list.append({'GUI':mini_GUI,'func':func})
        self.__list[-1]['GUI'].limits = self.limit_rect
        self.__list[-1]['GUI'].direccion(self.__list[-1]['GUI'].rect)

    
    def draw(self, surface,pos):
        for x in self.__list:
            x['GUI'].draw(surface,pos)

    def click(self, pos):
        for i, g in sorted(enumerate(self.__list),reverse=True):
            result = g['GUI'].click(pos)
            if result == 'exit':
                self.__list.pop(i)
                return False
            elif result or result == 0:
                self.__list.pop(i)
                if g['func']: g['func'](result)
                return result
            elif self.__list[i]['GUI'].rect.collidepoint(pos):
                self.__list.pop(i)
                self.__list.append(g)
                return 0



class Base:
    def __init__(self,pos,dir = 'center', size = (200,125), border_radius = 10) -> None:
        self.pos = Vector2(pos)
        self.dir = dir


        self.botones = [{
            'btn':Create_boton('X',24,None,(200,0),10,'topright', 'black', color_rect='lightgrey', color_rect_active='darkgrey', border_radius=0, border_top_right_radius=border_radius, border_width=-1),
            'result': 'exit',
            }]


        self.surf = pag.Surface(size,pag.SRCALPHA)
        self.rect = self.surf.get_rect()

        pag.draw.rect(self.surf, (240,240,240), [0,0,*size], 0, border_radius)
        pag.draw.rect(self.surf, 'lightgrey', [0,0,200,26], 0, border_top_left_radius=border_radius, border_top_right_radius=border_radius)

    def direccion(self, rect) -> None:
        rect.center = self.pos
        
        if self.dir == 'left':
            rect.left = self.pos[0]
        elif self.dir == 'right':
            rect.right = self.pos[0]
        elif self.dir == 'top':
            rect.top = self.pos[1]
        elif self.dir == 'bottom':
            rect.bottom = self.pos[1]
        elif self.dir == 'topleft':
            rect.left = self.pos[0]
            rect.top = self.pos[1]
        elif self.dir == 'topright':
            rect.right = self.pos[0]
            rect.top = self.pos[1]
        elif self.dir == 'bottomleft':
            rect.left = self.pos[0]
            rect.bottom = self.pos[1]
        elif self.dir == 'bottomright':
            rect.right = self.pos[0]
            rect.bottom = self.pos[1]
        if rect.right > self.limits.right:
            rect.right = self.limits.right
        elif rect.left < self.limits.left:
            rect.left = self.limits.left
        if rect.bottom > self.limits.bottom:
            rect.bottom = self.limits.bottom
        elif rect.top < self.limits.top:
            rect.top = self.limits.top

    def click(self,pos):
        for btn in self.botones:
            if btn['btn'].rect.collidepoint(Vector2(pos)-self.rect.topleft):
                return btn['result']

    def draw(self, surface,pos):
        for btn in self.botones:
            btn['btn'].draw(self.surf,Vector2(pos)-self.rect.topleft)
        surface.blit(self.surf,self.rect)

class simple_popup(Base):
    def __init__(self, pos, dir = 'center') -> None:

        super().__init__(pos,dir)

        Create_text('Hola :)', 20, None, (100,75), 'center', 'black').draw(self.surf)

        
        self.botones.append({
            'btn':Create_boton('Aceptar',16,None,(195,120), (20,10), 'bottomright','black','white', border_width=-1),
            'result': 'exit'
            })

class select(Base):
    def __init__(self, pos, options:list, dir = 'topleft', captured = None) -> None:

        self.pos = Vector2(pos)
        self.dir = dir
        self.texts = options
        self.captured = captured

        self.txt_tama = Create_boton(f'{options[0]}',16,None,(0,280), 6, 'topleft','white', (20,20,20), 'darkgrey', 0, 0, border_width=1, border_color='white').rect.h
        
        self.size = (125,self.txt_tama*len(options)+10)
        self.border_radius = 5
        self.botones: list[Create_text] = []

        self.surf = pag.Surface(self.size,pag.SRCALPHA)
        self.rect = self.surf.get_rect()

        for i, op in enumerate(options):
            self.botones.append(Create_text(f'{op}',16,None,(10,self.txt_tama*i +5), 'topleft','black', padding= 5))
    
    def draw(self,surface,pos):
        pag.draw.rect(self.surf, (240,240,240), [0,0,*self.size], 0, self.border_radius)
        if self.rect.collidepoint(pos):
            new_pos = Vector2(pos)-self.rect.topleft
            new_pos_selection = self.txt_tama*math.floor((new_pos.y/self.size[1])*len(self.texts)) + 5
            pag.draw.rect(self.surf, 'darkgrey', [0,new_pos_selection,self.size[0],self.txt_tama], 0, self.border_radius)
        for btn in self.botones:
            btn.draw(self.surf)
        surface.blit(self.surf,self.rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            new_pos = Vector2(pos)-self.rect.topleft
            final_index = math.floor((new_pos.y/self.size[1])*len(self.texts))
            return {'index': final_index, 'text': self.botones[final_index].get_text(), 'obj':self.captured}
        else:
            return 'exit'
