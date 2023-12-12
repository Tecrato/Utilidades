import pygame as pag, time
from pygame.surface import Surface
from pygame.math import Vector2
from pygame.locals import *

from .Animaciones import Second_Order_Dinamics

class Base:
    def create_border(self, rect, border_width) -> None:
        self.rect_border = pag.rect.Rect(0,0,rect.size[0] + border_width,rect.size[1] + border_width)
        self.rect_border.center = rect.center
    def direccion(self, rect) -> None:
        rect.center = self.pos
        
        if self.dire == 'left':
            rect.left = self.pos[0]
        elif self.dire == 'right':
            rect.right = self.pos[0]
        elif self.dire == 'top':
            rect.top = self.pos[1]
        elif self.dire == 'bottom':
            rect.bottom = self.pos[1]
        elif self.dire == 'topleft':
            rect.left = self.pos[0]
            rect.top = self.pos[1]
        elif self.dire == 'topright':
            rect.right = self.pos[0]
            rect.top = self.pos[1]
        elif self.dire == 'bottomleft':
            rect.left = self.pos[0]
            rect.bottom = self.pos[1]
        elif self.dire == 'bottomright':
            rect.right = self.pos[0]
            rect.bottom = self.pos[1]
            
    def smothmove(self, T, f, z, r) -> None:
        self.smothmove_pos = self.pos
        self.smothmove_bool = True
        self.movimiento = Second_Order_Dinamics(T, f, z, r, self.pos)

class Create_text(Base):
    """
    ### Comandos
    - draw() - Dibuja el texto\n
        - Si tu colocar border radius 10000 sera redondo\n
    - change_text() - Cambia el texto\n
    - change_color() - Cambia el color del texto\n
    - get_text() - Retorna el texto actual
    - move() - Mueve el texto al sitio seleccionado\n
    - smothmove() - permite una transicion suave en el movimiento utilizando la clase Second Order Dinamics
    """
    def __init__(self,text: str,size: int,font: str, pos: tuple,surface: Surface,dire='center',color='white',with_rect = False,color_rect ='black', **kwargs) -> None:
        
        pag.font.init()
        self.raw_text = text
        self.size = size
        self.raw_font = font
        self.pos = pos
        self.surface = surface
        self.dire = dire
        self.color = color
        self.with_rect = with_rect
        self.color_rect = color_rect
        padding = kwargs.get('padding',20)
        if isinstance(padding, tuple) or isinstance(padding, Vector2) or isinstance(padding, list):
            self.padding = Vector2(padding)
        else:
            self.padding = Vector2(padding,padding)
        self.rect_width = kwargs.get('rect_width',0)
        
        self.border_radius = kwargs.get('border_radius',0)
        self.border_top_left_radius = kwargs.get('border_top_left_radius',-1)
        self.border_bottom_left_radius = kwargs.get('border_bottom_left_radius',-1)
        self.border_top_right_radius = kwargs.get('border_top_right_radius',-1)
        self.border_bottom_right_radius = kwargs.get('border_bottom_right_radius',-1)
        self.border_width = kwargs.get('border_width', -1)
        self.border_color = kwargs.get('border_color', 'black')

        self.lista_text = []
        self.mode = 1
        self.font = pag.font.Font(self.raw_font, size)

        self.smothmove_bool=False

        try:
            if  isinstance(text, list): raise Exception('Es una lista')
            self.text = self.font.render(f'{text}', 1, self.color)
            self.rect_text = self.text.get_rect()
            self.rect = self.text.get_rect()
            self.rect.size = (self.rect.w + self.padding[0], self.rect.h + self.padding[1])
            if self.border_radius == 10000:
                self.rect.size = (max(self.rect_text.h * 1.2,self.rect_text.w * 1.2), max(self.rect_text.h * 1.2,self.rect_text.w * 1.2))
            self.rect.center = self.pos
            self.direccion(self.rect)
            self.rect_text.center = self.rect.center
            self.create_border(self.rect, self.border_width)
        except Exception as err:
            self.mode = 2
            self.text = self.font.render(f'{text[0]}', 1, color)
            self.rect_text = self.text.get_rect()
            self.rect = self.text.get_rect()
            self.direccion(self.rect_text)

            self.rect.center = self.rect_text.center

            for txt in range(len(self.raw_text)):
                self.lista_text.append(Create_text(self.raw_text[txt], size, font, (pos[0],pos[1] + self.rect.h*txt), surface, dire, color, False, color_rect, padding=padding, rect_width=self.rect_width, 
                    border_radius=self.border_radius, border_top_left_radius=self.border_top_left_radius, 
                    border_bottom_right_radius=self.border_bottom_right_radius, border_bottom_left_radius=self.border_bottom_left_radius, 
                    border_top_right_radius=self.border_top_right_radius, border_width=self.border_width, border_color=self.border_color))
            self.rect = self.text.get_rect()
            if self.border_radius == 10000:
                self.rect.size = (max(self.rect.h * len(self.raw_text) + self.padding[0],max(self.font.render(txt, 1, self.color).get_rect().width + self.padding[0] for txt in self.raw_text)), max(self.rect.h * len(self.raw_text) + self.padding[2],max(self.font.render(tixt, 1, self.color).get_rect().width + self.padding[1] for tixt in self.raw_text)))
            else:
                self.rect.width = min(max(self.font.render(tixt, 1, self.color).get_rect().width * 1.2 for tixt in self.raw_text), max(self.font.render(tixt, 1, self.color).get_rect().width + self.padding[0] for tixt in self.raw_text))
                self.rect.height = (self.rect_text.h * (len(self.raw_text)-1)) + self.padding[0]

            self.direccion(self.rect)
            self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2
            
            self.create_border(self.rect, self.border_width)

    def draw(self, surface=None) -> None:
        if surface != None:
            repuesto = self.surface
            self.surface = surface
        if self.smothmove_bool:
            pos = self.movimiento.update(self.smothmove_pos)
            self.pos = pos
            self.direccion(self.rect)

            if self.mode == 1:
                    self.rect_text.center = self.rect.center
            elif self.mode == 2:
                self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2

        if self.mode == 2:
            if self.with_rect:
                pag.draw.rect(self.surface, self.color_rect, self.rect, self.rect_width,self.border_radius
                    , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
                pag.draw.rect(self.surface, self.border_color, self.rect_border, self.border_width,self.border_radius
                    ,self.border_top_left_radius,self.border_top_right_radius,self.border_bottom_left_radius,self.border_bottom_right_radius)
            for txt in self.lista_text:
                txt.draw()
            return
        if self.with_rect:
            pag.draw.rect(self.surface, self.color_rect, self.rect, self.rect_width,self.border_radius
                , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
            pag.draw.rect(self.surface, self.border_color, self.rect_border, self.border_width,self.border_radius
                , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
        self.surface.blit(self.text, self.rect_text)

        if surface != None:
            self.surface = repuesto

    def change_text(self, text) -> None:
        self.lista_text.clear()
        self.raw_text = text
        if self.mode == 1:
            self.text = self.font.render(f'{text}', 1, self.color)
            self.rect_text = self.text.get_rect()
            self.rect = self.text.get_rect()
            self.rect.size = (self.rect.w + self.padding[0], self.rect.h + self.padding[1])
            if self.border_radius == 10000:
                self.rect.size = (max(self.rect_text.h * 1.2,self.rect_text.w * 1.2), max(self.rect_text.h * 1.2,self.rect_text.w * 1.2))
            self.rect.center = self.pos
            self.direccion(self.rect)
            
            self.rect_text.center = self.rect.center
        elif self.mode == 2:
            self.font = pag.font.Font(self.raw_font, self.size)
            self.text = self.font.render(f'{text[0]}', 1, self.color)
            self.rect_text = self.text.get_rect()
            self.rect = self.text.get_rect()
            self.direccion(self.rect_text)

            for txt in range(len(self.raw_text)):
                self.lista_text.append(Create_text(self.raw_text[txt], self.size, self.raw_font, (self.pos[0],self.pos[1] + self.rect.h*txt), self.surface, self.dire, self.color, False, self.color_rect, self.padding, self.rect_width, self.border_radius, self.border_top_left_radius, self.border_bottom_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius, self.border_width, self.border_color))
            self.rect = self.text.get_rect()
            if self.border_radius == 10000:
                self.rect.size = (max(self.rect.h * len(self.raw_text) * 1.23,max(self.font.render(tixt, 1, self.color).get_rect().width * 1.2 for tixt in self.raw_text)), max(self.rect.h * len(self.raw_text) * 1.2,max(self.font.render(tixt, 1, self.color).get_rect().width * 1.2 for tixt in self.raw_text)))
            else:
                self.rect.width = (min(max(self.font.render(tixt, 1, self.color).get_rect().width * 1.2 for tixt in self.raw_text), max(self.font.render(tixt, 1, self.color).get_rect().width + 20 for tixt in self.raw_text)))
                self.rect.height = (self.rect_text.h * (len(self.raw_text)-1)) + (self.rect_text.h * 1.2) 
            self.rect.center = (self.rect_text.centerx,self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2)

    def change_color(self, color) -> None:
        self.color = color
        if self.mode == 1:
            self.text = self.font.render(self.raw_text, 1, color)
        elif self.mode == 2:
            for txt in self.lista_text:
                txt.change_color(color)

    def move(self, pos, dire: str = None) -> None:
        if dire != None: self.dire = dire
        if self.smothmove_bool:
            self.smothmove_pos = pos
        else:
            self.pos = pos
            self.direccion(self.rect)

            if self.mode == 1:
                self.rect_text.center = self.rect.center
            elif self.mode == 2:
                for n, txt in enumerate(self.lista_text):
                    txt.move((pos[0],pos[1] + self.rect.h*n), dire)
                self.direccion(self.rect)
                self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2

    def get_text(self) -> str:
        return self.raw_text

    def __str__(self) -> str:
        return f'{self.raw_text = } - {self.pos = }'

class Create_boton(Create_text):
    def __init__(self, text, size: int, font: str, pos: tuple, surface: Surface, padding: int = 20,
        dire: str = 'center', color = 'black', color_rect = 'darkgrey',
        color_rect_active='lightgrey',rect_width=0,border_radius:int=15,border_top_left_radius:int=-1,
        border_top_right_radius: int = -1, border_bottom_left_radius: int = -1,
        border_bottom_right_radius: int = -1, border_width = 2, border_color = 'black', with_rect = True,
        func = None, **kwargs) -> None:

        self.color_rect_active = color_rect_active if color_rect_active != None else color_rect
        self.color_rect_inactive = color_rect
        self.color_inactive = color
        self.with_rect2 = with_rect

        self.toggle_rect = kwargs.get('toggle_rect',False)

        color_active = kwargs.get('color_active',None)
        self.color_active = color_active if color_active != None else color
        self.func = func
    
        self.sound_to_hover = kwargs.get('sound_to_hover',False)
        
        self.sound_to_click = kwargs.get('sound_to_click',False)

        Create_text.__init__(self,text, size, font, pos, surface, dire, color, with_rect, color_rect, padding=padding, 
                             rect_width=rect_width, border_radius=border_radius,border_top_left_radius=border_top_left_radius, 
                             border_top_right_radius=border_top_right_radius, border_bottom_left_radius=border_bottom_left_radius, 
                             border_bottom_right_radius=border_bottom_right_radius, border_width=border_width,border_color=border_color)
        if self.toggle_rect:
            self.with_rect = False
        self.hover = False

    def draw(self) -> None:
        if self.rect.collidepoint(pag.mouse.get_pos()):
            if not self.hover:
                if self.sound_to_hover:
                    self.sound_to_hover.play()
                self.hover = True
                self.color_rect = self.color_rect_active
                self.change_color(self.color_active)
                if self.toggle_rect and self.with_rect2:
                    self.with_rect = True
        else:
            if self.hover:
                self.hover = False
                self.color_rect = self.color_rect_inactive
                self.change_color(self.color_inactive)
                if self.toggle_rect and self.with_rect2:
                    self.with_rect = False
        super().draw()

    def click(self) -> None:
        if self.sound_to_click:
            self.sound_to_click.play()
        if self.func:
            self.func()
    def change_color_ad(self,color,color_active) -> None:
        self.color_inactive = color
        self.color_active = color_active if color_active != None else self.color_active
        if self.hover:
            self.change_color(self.color_active)
        else:
            self.change_color(self.color_inactive)

class Input_text(Base):
    def __init__(self, surface: Surface, pos: tuple, size: tuple, font: str, text_value: str = 'Type here',max_letter = 20, padding = 20,
        text_color = 'white', background_color = 'black', **kwargs) -> None:
        
        self.border_radius = kwargs.get('border_radius',0)
        self.border_top_left_radius = kwargs.get('border_top_left_radius',-1)
        self.border_bottom_left_radius = kwargs.get('border_bottom_left_radius',-1)
        self.border_top_right_radius = kwargs.get('border_top_right_radius',-1)
        self.border_bottom_right_radius = kwargs.get('border_bottom_right_radius',-1)
        self.border_width = kwargs.get('border_width', -1)
        self.border_color = kwargs.get('border_color', 'black')

        self.surface = surface
        self.size = Vector2(size)
        self.pos = pos
        if isinstance(padding, tuple) or isinstance(padding, Vector2) or isinstance(padding, list):self.padding = Vector2(padding)
        else: self.padding = Vector2(padding,padding)
        self.raw_text = ''
        self.max_letter = max_letter
        self.background_color = background_color


        self.text = Create_text(self.raw_text, size[0], font, pos, self.surface, 'left', padding=padding)
        self.text_rect = self.text.rect.copy()
        self.text_rect.w = size[1]
        self.create_border(self.text_rect, self.border_width)

        self.text = Create_text(self.raw_text, size[0], font, pos, self.surface, 'left', padding=5)
        self.text_rect2 = self.text.rect.copy()
        self.text_rect2.w = size[1] - self.padding.x
        self.text_rect2.left += self.padding.x/2
        self.input_surface = pag.surface.Surface(self.text_rect2.size, pag.SRCALPHA)
        self.text = Create_text(self.raw_text, size[0], font, (0,size[0]/2), self.input_surface, 'left', text_color, padding=0)


        self.text_value = Create_text(text_value, size[0], font, (0,size[0]/2), self.input_surface, 'left', 'gray', padding=0)

        self.typing = False
        self.typing_pos = 0
        self.backspace = False
        self.supr = False
        self.del_time = 0
        self.left_b = False
        self.left_time = 0
        self.right_b = False
        self.right_time = 0
        self.typing_line = True
        self.typing_line_time = time.time()

    def draw(self) -> None:
        if self.backspace and time.time() - self.del_time > .5:
            self.del_letter()
        if self.left_b and time.time() - self.left_time > .5:
            self.left()
        if self.right_b and time.time() - self.right_time > .5:
            self.right()
        pag.draw.rect(self.surface, self.background_color, self.text_rect, border_radius=self.border_radius)
        pag.draw.rect(self.surface, self.border_color, self.rect_border, self.border_width,self.border_radius
            , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
        self.input_surface.fill((0,0,0,0))

        # else:
        if self.typing:
            if time.time()-self.typing_line_time > .7:
                self.typing_line = not self.typing_line
                self.typing_line_time = time.time()
            if self.typing_line:
                self.text.change_text(self.raw_text[:self.typing_pos] + '|' + self.raw_text[self.typing_pos:])
            else:
                self.text.change_text(self.raw_text)
        elif self.raw_text == '': self.text_value.draw()
        self.text.draw()
                
        self.surface.blit(self.input_surface, self.text_rect2)

    def eventos_teclado(self, eventos):
        for evento in eventos:
            if self.typing:
                if evento.type == KEYDOWN:
                    if evento.key == K_LEFT:
                        self.left()
                    elif evento.key == K_RIGHT:
                        self.right()
                    elif evento.key == K_BACKSPACE:
                        self.del_letter()
                    elif evento.key == K_RETURN:
                        return "enter"
                elif evento.type == TEXTINPUT:
                    self.add_letter(evento.text)
                elif evento.type == KEYUP:
                    if evento.key == K_BACKSPACE:
                        self.backspace = False
                    elif evento.key == K_LEFT:
                        self.left_b = False
                    elif evento.key == K_RIGHT:
                        self.right_b = False
            if evento.type == MOUSEBUTTONDOWN:
                self.click()

    def click(self, pos = False) -> None:
        if pos:
            m = pos
        else:
            m = pag.mouse.get_pos()
        if self.text_rect.collidepoint(m): self.typing = True
        else:
            self.typing = False
            self.backspace = False

    def add_letter(self, t) -> None:
        if len(self.raw_text) < self.max_letter:
            self.raw_text = self.raw_text[:self.typing_pos] + t + self.raw_text[self.typing_pos:]
            self.typing_pos += 1
            self.text.change_text(self.raw_text)
            if self.text.rect_text.w > self.text_rect2.w:
                self.text.move((self.text_rect2.width,self.size[0]/2), 'right')
            else:
                self.text.move((0,self.size[0]/2), 'left')
        self.typing_line = True
        self.typing_line_time = time.time()

    def del_letter(self) -> None:
        if not self.backspace:
            self.backspace = True
            self.del_time = time.time()
        if len(str(self.raw_text)) > 0:
            if self.typing_pos == 0:
                return
            self.raw_text = self.raw_text = self.raw_text[:self.typing_pos-1] + self.raw_text[self.typing_pos:]
            self.typing_pos -= 1
            self.text.change_text(self.raw_text)
            if self.text.rect_text.w > self.text_rect2.w:
                self.text.move((self.text_rect2.width,self.size[0]/2), 'right')
            else:
                self.text.move((0,self.size[0]/2), 'left')
        self.typing_line = True
        self.typing_line_time = time.time()

    def left(self):
        if not self.left_b:
            self.left_b = True
            self.left_time = time.time()
        self.typing_pos = max(0,self.typing_pos -1)
        self.typing_line = True
        self.typing_line_time = time.time()

    def right(self):
        if not self.right_b:
            self.right_b = True
            self.right_time = time.time()
        self.typing_pos = min(len(self.raw_text),self.typing_pos + 1)
        self.typing_line = True
        self.typing_line_time = time.time()

    def set(self, text) -> None:
        self.raw_text = text + ' '
        self.typing_pos = len(str(self.raw_text))
        self.text.change_text(self.raw_text)
        self.backspace = False
        self.typing_line = True
        self.typing_line_time = time.time()

    def get_text(self) -> str:
        return self.raw_text
    
    def __str__(self) -> str:
        return f'{self.raw_text = } - {self.pos = } - {self.max_letter}'

class List_Box:
    def __init__(self, size: tuple, surface: Surface, pos: tuple, lista: list = None, text_size: int = 20, separation: int = -5,
        selected_color = (100,100,100,100), text_color= 'white', header: bool =False, text_header:str = None, **kwargs) -> None:

        self.size = Vector2(size)
        self.surface = surface
        self.pos = Vector2(pos)
        self.text_size = text_size
        self.separation = separation
        self.smothscroll = kwargs.get('smothscroll',True)
        self.background_color = kwargs.get('background_color','black')
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.with_index = kwargs.get('with_index',False)
        self.text_color = text_color
        self.header = header
        self.text_header = text_header

        self.lista_palabras = ['None', 'None', 'None'] if lista == None or lista == [] else lista
        self.lista_objetos = []

        if self.header:
            self.text_header = Create_text(self.text_header, text_size, None, pos, self.surface, 'topleft', 'black', True, 'darkgrey',
            padding=(20,15),border_width=1, border_top_left_radius=kwargs.get('header_top_left_radius'), border_top_right_radius=kwargs.get('header_top_right_radius'))
            self.text_header.rect.w = size[0]
            self.text_header.rect_border.w = size[0]+1
            self.pos = Vector2(pos[0], pos[1]+self.text_header.rect.h)
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1], size[0], size[1]-self.text_header.rect.h)
        else:
            self.rect = pag.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.lista_surface= pag.surface.Surface(self.rect.size, SRCALPHA)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = pos

        self.desplazamiento = 0
        self.total_height = 0
        self.movimiento = None
        self.smothmove_bool = False
        self.el_elegido = False

        self.actualizar()
        self.scroll_bar_active = kwargs.get('scroll_bar_active',True)
        if self.scroll_bar_active:
            #Scrollbar
            #La barra entera
            self.bar = pag.rect.Rect(self.lista_surface_rect.w - 10, 0, 10, self.lista_surface_rect.h)
            self.bar_surface = pag.Surface(self.bar.size, pag.SRCALPHA)
            self.bar_surface.fill((255,255,255,128))

            #La barra que sube y baja
            self.barra = pag.rect.Rect(self.lista_surface_rect.w - 10, 0, 10, 50)
        self.scroll = False

        #cuadro de seleccion
        self.select_box = pag.rect.Rect(0,-5000,self.lista_surface_rect.w,self.text_size + self.separation)
        self.selected_num = -1

    def draw(self) -> None:
        if self.header:
            self.text_header.draw()
        self.lista_surface.fill(self.background_color)
        pag.draw.rect(self.lista_surface, self.selected_color, self.select_box)
        self.select_box.centery = self.lista_objetos[self.selected_num].rect.centery if self.selected_num != -1 else self.lista_surface_rect.h + self.select_box.h
        for te in self.lista_objetos:
            # if self.smothscroll == True:
            te.draw()
            # else:
                # n = self.lista_surface_rect.copy()
                # n.topleft = (0,0)
                # if n.collidepoint(te.rect.center):
                #     te.draw()
        if self.scroll:
            self.scroll_func()
            
        if self.total_height + self.lista_surface_rect.h > self.rect.h and self.scroll_bar_active:
            pag.draw.rect(self.lista_surface, 'white', self.barra)
            self.lista_surface.blit(self.bar_surface, self.bar.topleft)

        if self.smothmove_bool:
            self.pos = self.movimiento.update(self.smothmove_pos)
            self.rect.topleft = self.pos

        self.surface.blit(self.lista_surface,self.rect)

    def move(self, pos) -> None:
        if self.smothmove_bool:
            self.smothmove_pos = pos
        else:
            self.pos = pos
            self.rect.topleft = self.pos

    def rodar(self,y) -> None:
        if self.total_height + self.lista_surface_rect.h < self.rect.h:
            return

        self.desplazamiento += y
        if self.scroll_bar_active:
            self.barra.top = -(self.lista_surface_rect.h-self.barra.h) * (self.desplazamiento/self.total_height)
        if self.desplazamiento > 1:
            self.desplazamiento = self.padding_top
            if self.scroll_bar_active:
                self.barra.top = 0
        elif self.desplazamiento < -self.total_height:
            self.desplazamiento = -self.total_height
            if self.scroll_bar_active:
                self.barra.bottom = self.rect.h
        
        for num ,text in enumerate(self.lista_objetos):
            text.move((self.padding_left,(self.text_size + self.separation) * num + self.desplazamiento))

    def actualizar(self) -> None:
        self.lista_objetos.clear()
        for num ,text in enumerate(self.lista_palabras):
            if self.with_index:
                self.lista_objetos.append(Create_text(f'{num}) {text}', self.text_size, None, (self.padding_left,(self.text_size + self.separation) * num + self.padding_top), self.lista_surface, 'topleft', self.text_color))
            else:
                self.lista_objetos.append(Create_text(text, self.text_size, None, (self.padding_left,(self.text_size + self.separation) * num + self.padding_top), self.lista_surface, 'topleft', self.text_color))
        self.total_height = 0
        if self.smothscroll:
            for x in self.lista_objetos:
                x.smothmove(1/60, 1.5, 1, 1.5)
        self.total_height = self.lista_objetos[-1].rect.bottom - self.lista_surface_rect.h

    def change_list(self, lista) -> None:
        self.lista_palabras = ['None', 'None', 'None'] if lista == None or lista == [] else lista
        if self.scroll_bar_active:
            self.select_box.top = self.rect.bottom
        self.actualizar()

    def select(self, index: int = -2000, pos = None, driff = True) -> str:
        if pos == None:
            m = Vector2(pag.mouse.get_pos())
            m -= self.pos
            if self.header: m += (0,10)
        else:
            m = Vector2(pos)
        if isinstance(index, str):
            self.select_box.top = self.lista_surface_rect.h
            return False
        elif index != -2000:
            self.select_box.centery = self.lista_objetos[index].rect.centery
            self.selected_num=index
            if driff:
                self.desplazamiento = (-(self.text_size + self.separation) * index + self.padding_top) + self.lista_surface_rect.h/2
            self.rodar(0)
            return {'text': self.lista_objetos[index].raw_text, 'index': index}
        if self.total_height + self.lista_surface_rect.h > self.rect.h and self.scroll_bar_active and self.barra.collidepoint(m - (0,10)):
            self.scroll = True
            return 'scrolling'
        for index, te in enumerate(self.lista_objetos):
            if te.rect.collidepoint(m):
                self.select_box.centery = te.rect.centery
                self.selected_num = index
                return {'text': te.get_text(), 'index': index}
        self.selected_num=-1
        return False

    def scroll_func(self) -> None:
        if self.el_elegido:
            m = Vector2(pag.mouse.get_pos()) - self.segunda_pos
        else:
            m = Vector2(pag.mouse.get_pos())
            m -= self.pos

        self.barra.centery = m.y
        self.desplazamiento = -self.total_height *(self.barra.top / (self.lista_surface_rect.h-self.barra.h))

        if self.desplazamiento > 0:
            self.desplazamiento = self.padding_top
            self.barra.top = 0
        elif self.desplazamiento < -self.total_height:
            self.desplazamiento = -self.total_height
            self.barra.bottom = self.rect.h

        for num ,text in enumerate(self.lista_objetos):
            text.move((self.padding_left,(self.text_size + self.separation) * num + self.desplazamiento))

class Multi_list(Base):
    def __init__(self, size:tuple,surface:Surface,pos:tuple,num_lists:int=2,lista: list = None, text_size: int = 20, separation: int = -5,
        smothscroll: bool = True, background_color = 'black', selected_color = (100,100,100,100), text_color= 'white', colums_witdh= .33, header: bool =True, header_text: list = None, **kwargs) -> None:
        
        self.size = Vector2(size)
        self.surface = surface
        self.pos = Vector2(pos)
        self.lista_palabras = ['None', 'None', 'None'] if lista == None else lista
        self.text_size = text_size
        self.separation = separation
        self.smothscroll = smothscroll
        self.background_color = background_color
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.with_index = kwargs.get('with_index',False)
        self.text_color = text_color
        if num_lists <= 0: raise Exception('\n\nComo vas a hacer 0 listas en una multilista\nPensá bro...')
        self.num_list = num_lists
        self.colums_witdh = [.33 for x in range(self.num_list)] if colums_witdh == .33 else list(colums_witdh)
        self.colums_witdh.append(1)
        self.header = header
        self.text_header = [None for x in range(num_lists)] if header_text == None else header_text
        self.header_radius = kwargs.get('header_radius',0)
        self.border_color = kwargs.get('border_color', 'black')

        self.listas = []
        self.lineas = []
        self.scroll = False
        self.smothmove_bool = False

        self.rect = pag.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.lista_surface= pag.surface.Surface(self.rect.size, SRCALPHA)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = self.pos
        for x in range(num_lists):
            self.lineas.append([((self.size.x*self.colums_witdh[x] -1),0 if not self.header else -20), ((self.size.x*self.colums_witdh[x] -1),self.rect.h)])
            self.listas.append(List_Box(((self.size.x*self.colums_witdh[x+1]) - (self.size.x*self.colums_witdh[x]), self.size.y), 
                self.lista_surface,(self.size.x*self.colums_witdh[x],0), self.lista_palabras, self.text_size, self.separation, 
                self.selected_color, self.text_color, background_color=(0,0,0,0), smothscroll=self.smothscroll, padding_top=self.padding_top, padding_left=self.padding_left,with_index=self.with_index, 
                scroll_bar_active=False if x != num_lists-1 else True,
                header=True, text_header=self.text_header[x], header_top_left_radius=20 if x == 0 else 0, header_top_right_radius=20 if x == self.num_list-1 else 0))
        self.listas[-1].el_elegido = True
        self.listas[-1].segunda_pos = self.pos + (0,0 if not self.header else 20) + (0,25)

    def draw(self) -> None:
        if self.smothmove_bool:
            self.pos = self.movimiento.update(self.smothmove_pos)
            self.rect.topleft = self.pos
        self.lista_surface.fill(self.background_color)
        if self.header:
            pag.draw.rect(self.lista_surface, (0,0,0,0), pag.rect.Rect(0,0,self.rect.w, 20))
        for x in self.listas:
            x.draw()
        if self.scroll:
            for x in self.listas[:-1]:
                x.desplazamiento = self.listas[-1].desplazamiento
                x.rodar(0)
        for line in self.lineas[1:]:
            pag.draw.line(self.lista_surface, self.border_color, line[0], line[1], 2)
        for x in self.listas:
            pag.draw.rect(self.lista_surface, self.border_color, x.rect, 1)
        self.surface.blit(self.lista_surface,self.rect)

    def rodar(self,y) -> None:
        for x in self.listas:
            x.rodar(y)

    def actualizar(self) -> None:
        for x in self.listas:
            x.actualizar()

    def change_list(self, lista) -> None:
        for i,x in enumerate(self.listas):
            try:
                x.change_list(lista[i])
            except:
                x.change_list(None)

    def select(self, index: int = -2000) -> str:
        m = Vector2(pag.mouse.get_pos())
        m -= self.pos
        for x in self.listas:
            a = x.select(index,m - x.pos, False)
            if a == 'scrolling':
                self.scroll = True
            elif a != False:
                minilista = []
                for l in self.listas:
                    minilista.append(l.select(int(a['index']), m - x.pos, False)['text'])
                return minilista

    def detener_scroll(self) -> None:
        self.scroll = False
        for x in self.listas:
            x.scroll = False
