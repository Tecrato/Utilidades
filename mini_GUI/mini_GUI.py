import pygame as pag, math

from ..text import Create_boton, Create_text
from ..obj_Base import Base as primary_base
from pygame.math import Vector2



class mini_GUI_admin:
    def __init__(self, limit: pag.Rect) -> None:
        self.__list = []
        self.__limit = limit
    
    def add(self,mini_GUI,func=None,raw_pos=None):
        self.__list.append({'GUI':mini_GUI,'func':func,'raw_pos':raw_pos})
        self.__list[-1]['GUI'].limits = self.limit
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
                return False
    
    def clear(self):
        self.__list.clear()
    
    @property
    def limit(self):
        return self.__limit
    @limit.setter
    def limit(self,limit):
        self.__limit = limit
        for x in self.__list:
            x['GUI'].limits = self.__limit
            if x['raw_pos']:
                x['GUI'].pos = x['raw_pos']
            else:
                x['GUI'].pos = x['GUI'].pos



class Base(primary_base):
    def __init__(self,pos,dir = 'center', size = (200,125), border_radius = 10, inside_limits=True) -> None:
        self.limits = pag.Rect(0,0,600,550)
        self.inside_limits = inside_limits
        super().__init__(pos,dir)

        self.botones = [{
            'btn':Create_boton('X',24,None,(size[0],0),10,'topright', 'black', color_rect='lightgrey', color_rect_active='darkgrey', border_radius=0, border_top_right_radius=border_radius, border_width=-1),
            'result': 'exit',
            }]


        self.surf = pag.Surface(size,pag.SRCALPHA)
        self.rect = self.surf.get_rect()

        pag.draw.rect(self.surf, (240,240,240), [0,0,*size], 0, border_radius)
        pag.draw.rect(self.surf, 'lightgrey', [0,0,size[0],26], 0, border_top_left_radius=border_radius, border_top_right_radius=border_radius)

    def direccion(self, rect) -> None:
        rect.center = self.pos
        primary_base.direccion(self,rect)
        if not self.inside_limits:
            return
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
    def __init__(self, pos, dir = 'center', title= 'Titulo', text= 'Texto aqui', size= (200,80), border_radius=10, inside_limits=True) -> None:

        super().__init__(pos,dir, size, border_radius, inside_limits)

        Create_text(title, 16, None, (0,0), 'topleft', 'black').draw(self.surf)
        Create_text(text, 16, None, (10,40), 'left', 'black').draw(self.surf)

        
        self.botones.append({
            'btn':Create_boton('Aceptar',16,None,self.rect.bottomright, (20,15), 'bottomright','black',(240,240,240), border_radius=10, border_bottom_right_radius=0, border_width=-1),
            'result': 'exit'
            })
class desicion_popup(Base):
    def __init__(self, pos, title= 'Titulo', text= 'Texto aqui', size= (200,80),accept_boton_text= 'aceptar', dir = 'center', border_radius=10, inside_limits=True) -> None:

        super().__init__(pos,dir, size, border_radius, inside_limits)

        Create_text(title, 16, None, (0,0), 'topleft', 'black').draw(self.surf)
        Create_text(text, 16, None, (10,40), 'left', 'black').draw(self.surf)

        
        self.botones.append({
            'btn':Create_boton('Cancelar',16,None,self.rect.bottomright, (20,15), 'bottomright','black',(240,240,240), border_radius=10, border_bottom_right_radius=0, border_width=-1),
            'result': 'exit'
            })
        self.botones.append({
            'btn':Create_boton(accept_boton_text,16,None,(self.botones[1]['btn'].rect.left - 10,self.rect.bottom), (20,15), 'bottomright','black',(240,240,240), border_radius=10, border_bottom_right_radius=0, border_width=-1),
            'result': 'aceptar'
            })

class select(Base):
    def __init__(self, pos, options:list, dir = 'topleft', captured = None,min_width =0, border_radius=10, inside_limits=True) -> None:
        super().__init__(pos,dir, border_radius=border_radius, inside_limits=inside_limits)
        self.texts = options
        self.captured = captured
        self.botones: list[Create_text] = []

        self.txt_tama_h = Create_boton(f'{max([f'{x}' for x in options])}',16,None,(0,280), 6, 'topleft','white', (20,20,20), 'darkgrey', 0, 0, border_width=1, border_color='white').rect.h
        self.txt_tama_w = min_width
        
        for i, op in enumerate(options):
            t = Create_text(f'{op}',16,None,(10,self.txt_tama_h*i +5), 'topleft','black', padding= (0,5))
            self.txt_tama_w = max(self.txt_tama_w,t.width + 20)
            self.botones.append(t.copy())

        self.size = (self.txt_tama_w,(self.txt_tama_h*len(options))+10)
        self.border_radius = 5

        self.surf = pag.Surface(self.size,pag.SRCALPHA)
        self.rect = self.surf.get_rect()

    
    def draw(self,surface,pos):
        pag.draw.rect(self.surf, (240,240,240), [0,0,*self.size], 0, self.border_radius)
        if self.rect.collidepoint(pos):
            new_pos = Vector2(pos)-self.rect.topleft
            new_pos_selection = self.txt_tama_h*math.floor((new_pos.y/self.size[1])*len(self.texts)) + 5
            pag.draw.rect(self.surf, 'darkgrey', [0,new_pos_selection,self.size[0],self.txt_tama_h], 0, self.border_radius)
        for btn in self.botones:
            btn.draw(self.surf)
        surface.blit(self.surf,self.rect)

    def click(self, pos):
        if self.rect.collidepoint(pos):
            new_pos = Vector2(pos)-self.rect.topleft
            final_index = math.floor((new_pos.y/self.size[1])*len(self.texts))
            return {'index': final_index, 'text': self.botones[final_index].text, 'obj':self.captured}
        else:
            return 'exit'
