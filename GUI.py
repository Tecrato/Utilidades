import pygame as pag

from .text import Create_boton, Create_text, Input_text
from .hipotenuza import Vector2

class GUI_admin:
    def __init__(self,surface) -> None:
        self.surface = surface
        self.__list = []
        self.active = -1
    def add(self,clase) -> None:
        self.__list.append(clase.copy())
        self.active = 0
    def draw(self,surface) -> None:
        if self.active >= 0:
            self.__list[self.active].draw(surface)
    def click(self):
        for i, x in enumerate(self.__list):
            result = x.click()
            if result == 'destroy':
                self.__list.pop(i)
                self.active = -1 if not self.__list else 0
                return 'destroy'
            elif result:
                return result
        return False
    def pop(self,index=-1) -> None:
        if len(self.__list) > 0:
            self.__list.pop(index)
            self.active = -1 if not self.__list else 0
    def input_update(self,eventos):
        for x in self.__list:
            if isinstance(x,Text_return):
                x.update(eventos)

class Base_win:
    def __init__(self, centro) -> None:
        self.rect = pag.Rect(0,0,500,300)
        self.rect.center = centro
        self.topleft = Vector2(*self.rect.topleft) - (Vector2(*self.rect.topleft)*(2,2))

        self.surface = pag.Surface((500,300))
        self.surface.fill('white')
        pag.draw.rect(self.surface,'lightgrey',[0,0,500,40])

        self.state = 'minimized' # minimized | maximized

        self.botones = [
            {'btn':Create_boton('X',30,None,(500,0),20,'topright', 'black',with_rect=False),'result': 'destroy'},
        ]

        self.inputs:list[Input_text] = []
        

    def draw(self, surface: pag.Surface) -> None:
        [inp.draw(self.surface) for inp in self.inputs]
        [btn['btn'].draw(self.surface,self.topleft + pag.mouse.get_pos()) for btn in self.botones]
        surface.blit(self.surface,self.rect)

    def click(self):
        for inp in self.inputs:
            inp.click()

        for btn in self.botones:
            if btn['btn'].rect.collidepoint(*(self.topleft + pag.mouse.get_pos())):
                return btn['result']

    def copy(self):
        return self

class Info(Base_win):
    def __init__(self,centro: tuple[int,int],encabezado: str,text: str|list[str]):
        super().__init__(centro)

        Create_text(encabezado,40,None,(250,70),'center', 'black').draw(self.surface)
        Create_text(text,25,None,(30,120),'left', 'black').draw(self.surface)



class Text_return(Base_win):
    def __init__(self, centro, texto) -> None:
        super().__init__(centro)
        
        Create_text(texto,30,None,(250,70),'center', 'black').draw(self.surface)
        self.input = Input_text((175,150),(20,150), None)
        self.input.draw(self.surface)

        self.botones.append({
            'btn':Create_boton('Aceptar',30,None,(350,280), 20, 'bottomright','black','white', border_width=-1),
            'result':{'state':'done','text':lambda: self.input.get_text()}
            })
        self.botones.append(
            {'btn':Create_boton('Cancelar',30,None,(480,280), 20, 'bottomright','black','white', border_width=-1),'result':'cancelar'},
        )
        self.inputs.append(self.input)
        
    def draw(self,surface) -> None:
        self.input.draw(self.surface)
        super().draw(surface)

    def update(self,eventos) -> None:
        for inp in self.inputs:
            inp.eventos_teclado(eventos,offset=(Vector2(*self.rect.topleft) - (Vector2(*self.rect.topleft)*(2,2))) - pag.mouse.get_pos())

        