import pygame as pag

from .text import Create_boton, Create_text, Input_text
from pygame.math import Vector2

class GUI_admin:
    def __init__(self,surface) -> None:
        self.surface = surface
        self.__list = []
        self.active = -1
    def add(self,clase, func= None) -> None:
        self.__list.append({'GUI':clase.copy(), 'func':func})
        self.active = len(self.__list)-1
    def draw(self,surface, mouse_pos) -> None:
        if self.active >= 0:
            self.__list[self.active]['GUI'].draw(surface, mouse_pos)
    def click(self, pos):
        mx,my = pos
        result = self.__list[self.active]['GUI'].click((mx,my))
        if result and result['return'] == 'aceptar':
            if self.__list[self.active]['func']: self.__list[self.active]['func'](result['result']())
            self.pop(self.active)
            self.active = -1 if not self.__list else 0
            return (self.active,result['result']())
        elif result and result['return'] in ['destroy', 'cancelar']:
            # if self.__list[self.active]['func']: self.__list[self.active]['func'](False)
            self.pop(self.active)
            self.active = -1 if not self.__list else 0
            return False
        return False
    def pop(self,index=-1) -> None:
        if len(self.__list) > 0:
            self.__list.pop(index)
            self.active = len(self.__list)-1
    def input_update(self,eventos):
        for x in self.__list:
            if isinstance(x['GUI'],Text_return):
                x['GUI'].update(eventos)

class Base_win:
    def __init__(self, centro, title) -> None:
        self.rect = pag.Rect(0,0,500,300)
        self.rect.center = centro

        # self.topleft = Vector2(self.rect.topleft) - (Vector2(self.rect.topleft)*(2,2))

        self.surface: pag.Surface = pag.Surface((500,300), pag.SRCALPHA)
        pag.draw.rect(self.surface,'white',[0,0,500,300], border_radius=20)
        pag.draw.rect(self.surface,'lightgrey',[0,0,500,40], border_top_left_radius=20, border_top_right_radius=20)
        Create_text(title, 30, None, (0,0), 'topleft', 'black', False).draw(self.surface)

        self.state: str = 'minimized' # minimized | maximized
        self.pressed_click: bool = False

        self.botones = [{
            'btn':Create_boton('X',30,None,(500,0),20,'topright', 'black', color_rect='lightgrey', color_rect_active='darkgrey', border_radius=0, border_top_right_radius=20, border_width=-1),
            'return': 'destroy',
            'result': lambda:'',
            }]

        self.inputs:list[Input_text] = []
        

    def draw(self, surface: pag.Surface, mouse_pos) -> None:
        mx,my = Vector2(mouse_pos)-self.rect.topleft
        [inp.draw(self.surface) for inp in self.inputs]
        [btn['btn'].draw(self.surface,(mx,my)) for btn in self.botones]
        surface.blit(self.surface,self.rect)

    def click(self, pos):
        mx,my = Vector2(pos)-self.rect.topleft
        for inp in self.inputs:
            inp.click((mx,my))

        for btn in self.botones:
            if btn['btn'].rect.collidepoint((mx,my)):
                return btn
            
        if pag.Rect([0,0,500,40]).collidepoint((mx,my)):
            self.pressed_click = True

    def copy(self):
        return self

class Info(Base_win):
    def __init__(self,centro: tuple[int,int],encabezado: str,text: str|list[str]):
        super().__init__(centro,encabezado)

        # Create_text(encabezado,40,None,(250,70),'center', 'black').draw(self.surface)
        Create_text(text,25,None,(30,120),'left', 'black').draw(self.surface)

        self.botones.append({
            'btn':Create_boton('Aceptar',30,None,(480,280), 20, 'bottomright','black','white', border_width=-1),
            'return':'aceptar',
            'result': lambda: True
            })
        
class Desicion(Base_win):
    def __init__(self,centro: tuple[int,int],encabezado: str,text: str|list[str]):
        super().__init__(centro,encabezado)

        # Create_text(encabezado,40,None,(250,70),'center', 'black').draw(self.surface)
        Create_text(text,25,None,(30,120),'left', 'black').draw(self.surface)

        self.botones.append({
            'btn':Create_boton('Aceptar',30,None,(350,280), 20, 'bottomright','black','white', border_width=-1),
            'return':'aceptar',
            'result': lambda: True
            })
        self.botones.append({
            'btn':Create_boton('Cancelar',30,None,(480,280), 20, 'bottomright','black','white', border_width=-1),
            'return':'cancelar',
            'result': lambda: 'cancelar'
            })



class Text_return(Base_win):
    def __init__(self, centro, encabezado, texto) -> None:
        super().__init__(centro, encabezado)
        
        Create_text(texto,30,None,(250,70),'center', 'black').draw(self.surface)
        self.input = Input_text((175,150),(20,150), None)
        self.input.draw(self.surface)

        self.botones.append({
            'btn':Create_boton('Aceptar',30,None,(350,280), 20, 'bottomright','black','white', border_width=-1),
            'return':'aceptar',
            'result': lambda: self.input.get_text()
            })
        self.botones.append({
            'btn':Create_boton('Cancelar',30,None,(480,280), 20, 'bottomright','black','white', border_width=-1),
            'return':'cancelar',
            'result': lambda:'cancelar'
        })
        self.inputs.append(self.input)
        
    def draw(self,surface, mouse_pos) -> None:
        self.input.draw(self.surface)
        super().draw(surface, mouse_pos)
    
    def update(self,eventos) -> None:
        for inp in self.inputs:
            inp.eventos_teclado(eventos,offset=self.rect.topleft)

        