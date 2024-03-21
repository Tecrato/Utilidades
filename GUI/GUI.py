import pygame as pag, pyperclip

from ..text import Create_boton, Create_text, Input_text
from pygame.math import Vector2

configs = {}

class GUI_admin:
    """
    # Ejemplo:

    ### Para los eventos de los inputs:
    self.GUI_manager.input_update(eventos)

    ### Para los eventos:
    (Debajo del evento de QUIT)
    elif self.GUI_manager.active >= 0:
        if evento.type == KEYDOWN and evento.key == K_ESCAPE:
            self.GUI_manager.pop()
        elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
            self.GUI_manager.click((mousex,mousey))

    ### Para dibujar:
    self.GUI_manager.draw(self.ventana,(mousex,mousey))
    """
    def __init__(self) -> None:
        self.__list = []
        self.active = -1
        try:
            configs['fuente_simbolos']
        except Exception as err:
            raise Exception('Debes incluir la siguiente linea de codigo: Utilidades.GUI.configs[\'fuente_simbolos\'] = "tu path hasta la fuente de symbols"')
    def add(self,clase, func= None) -> None:
        self.__list.append({'GUI':clase.copy(), 'func':func})
        self.active = len(self.__list)-1
    def draw(self,surface, mouse_pos) -> None:
        if self.active >= 0:
            self.__list[self.active]['GUI'].draw(surface, mouse_pos)
    def click(self, pos):
        mx,my = pos
        result = self.__list[self.active]['GUI'].click((mx,my))
        if result and result['return'] in ['aceptar','cancelar']:
            if self.__list[self.active]['func']: self.__list[self.active]['func'](result['result']())
            self.pop(self.active)
            self.active = -1 if not self.__list else 0
            return (self.active,result['result']())
        elif result and result['return'] in ['destroy']:
            self.pop(self.active)
            self.active = -1 if not self.__list else 0
            return False
        elif result and result['return'] == 'function':
            result['result']()
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
    def __init__(self, centro, title, size:tuple[int,int]=(500,300)) -> None:
        self.rect = pag.Rect(0,0,*size)
        self.rect.center = centro
        self.size = size


        self.surface: pag.Surface = pag.Surface(size)
        self.surface.fill((254,1,1))
        self.surface.set_colorkey((254,1,1))
        pag.draw.rect(self.surface,'white',[0,0,*size], border_radius=20)
        pag.draw.rect(self.surface,'lightgrey',[0,0,size[0],40], border_top_left_radius=20, border_top_right_radius=20)
        Create_text(title, 30, None, (0,0), 'topleft', 'black', False).draw(self.surface)

        self.state: str = 'minimized' # minimized | maximized
        self.pressed_click: bool = False

        self.botones = [{
            'btn':Create_boton('X',30,None,(size[0],0),20,'topright', 'black', color_rect='lightgrey', color_rect_active='darkgrey', border_radius=0, border_top_right_radius=20, border_width=-1),
            'return': 'destroy',
            'result': lambda:'',
            }]

        self.inputs:list[Input_text] = []
        

    def draw(self, surface: pag.Surface, mouse_pos) -> None:
        mx,my = Vector2(mouse_pos)-self.rect.topleft
        [inp.draw(self.surface) for inp in self.inputs]
        [btn['btn'].draw(self.surface,(mx,my)) for btn in self.botones]
        surface.blit(self.surface,self.rect)
        pag.draw.rect(surface,'black', self.rect,3, 20)

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

        Create_text(text,25,None,(30,120),'left', 'black').draw(self.surface)

        self.botones.append({
            'btn':Create_boton('Aceptar',30,None,Vector2(size)-(20,20), 20, 'bottomright','black','white', border_width=-1),
            'return':'aceptar',
            'result': lambda: True
            })
        
class Desicion(Base_win):
    def __init__(self,centro: tuple[int,int],encabezado: str,text: str|list[str], size=(500,300)):
        super().__init__(centro,encabezado,size)

        Create_text(text,25,None,(30,size[1]/2.3),'left', 'black').draw(self.surface)

        self.botones.append({
            'btn':Create_boton('Cancelar',24,None,Vector2(size)-(20,20), 15, 'bottomright','black','white', border_width=-1),
            'return':'cancelar',
            'result': lambda: 'cancelar'
            })
        self.botones.append({
            'btn':Create_boton('Aceptar',24,None,(Vector2(size)-(20,20))-(self.botones[1]['btn'].rect.w+20,0), 15, 'bottomright','black','white', border_width=-1),
            'return':'aceptar',
            'result': lambda: 'aceptar'
            })

class Text_return(Base_win):
    def __init__(self, centro, encabezado, texto, large=False) -> None:
        super().__init__(centro, encabezado)
        
        Create_text(texto,30,None,(250,50),'center', 'black').draw(self.surface)
        if large:
            self.input = Input_text((50,150),(20,375), None, border_top_left_radius=20, border_bottom_left_radius=20, max_letter=400)
        else:
            self.input = Input_text((175,150),(20,150), None, border_top_left_radius=20, border_bottom_left_radius=20, max_letter=40)

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
        self.botones.append({
            'btn':Create_boton('',25,configs['fuente_simbolos'],(425,150)if large else (325,150), (20,7), 'left','black','white', border_width=1, border_radius=0, border_top_right_radius=20, border_bottom_right_radius=20),
            'return':'function',
            'result': lambda: self.input.set(pyperclip.paste())
        })
        self.inputs.append(self.input)
        
    def draw(self,surface, mouse_pos) -> None:
        self.input.draw(self.surface)
        super().draw(surface, mouse_pos)
    
    def update(self,eventos) -> None:
        for inp in self.inputs:
            inp.eventos_teclado(eventos)

        