import pygame as pag, time
from pygame.math import Vector2

from .mytime import tener_el_tiempo

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
        self.smothmove_bool = True
        self.smothmove_pos = self.pos
        self.movimiento = Second_Order_Dinamics(T, f, z, r, self.pos)
    def normal_move(self) -> None:
        self.smothmove_bool = False


class Create_text(Base):
    """
    # Atributos extras

    ### Comandos
    - draw() - Dibuja el texto\n
        - Si colocas border radius 10_000 sera redondo\n
    - change_text() - Cambia el texto\n
    - change_color() - Cambia el color del texto\n
    - get_text() - Retorna el texto actual
    - move() - Mueve el texto al sitio seleccionado\n
    - smothmove() - permite una transicion suave en el movimiento utilizando la clase Second Order Dinamics
    """
    def __init__(self,text: str,size: int,font: str, pos: tuple,dire='center',color='white',with_rect = False
                 ,color_rect ='black', border_width = -1, **kwargs) -> None:
        
        pag.font.init()
        text = str(text)
        self.raw_text = text.replace('\t', '    ').split('\n') if '\n' in text else text
        self.size = size
        self.raw_font = font
        self.pos = Vector2(pos)
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
        self.border_width = border_width
        self.border_color = kwargs.get('border_color', 'black')

        self.lista_text = []
        self.mode = 1
        self.font = pag.font.Font(self.raw_font, size)

        self.smothmove_bool=False

        try:
            if  isinstance(self.raw_text, list): raise Exception('Es una lista')
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
            self.text_lines = len(self.raw_text)
            self.text_height = self.text.get_rect().h
            self.rect_text = self.text.get_rect()
            self.rect = self.text.get_rect()
            self.direccion(self.rect_text)

            self.rect.center = self.rect_text.center

            for txt in range(len(self.raw_text)):
                self.lista_text.append(Create_text(self.raw_text[txt], size, font, (pos[0],pos[1] + self.rect.h*txt), dire, color, False, color_rect, padding=padding, rect_width=0))
            self.rect = self.text.get_rect()
            if self.border_radius == 10000:
                self.rect.size = (max(self.rect.h * len(self.raw_text) + self.padding[0],max(self.font.render(txt, 1, self.color).get_rect().width + self.padding[0] for txt in self.raw_text)), max(self.rect.h * len(self.raw_text) + self.padding[2],max(self.font.render(tixt, 1, self.color).get_rect().width + self.padding[1] for tixt in self.raw_text)))
            else:
                self.rect.width = min(max(self.font.render(tixt, 1, self.color).get_rect().width * 1.2 for tixt in self.raw_text), max(self.font.render(tixt, 1, self.color).get_rect().width + self.padding[0] for tixt in self.raw_text))
                self.rect.height = (self.rect_text.h * (len(self.raw_text)-1)) + self.padding[0]

            self.direccion(self.rect)
            self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2
            
            self.create_border(self.rect, self.border_width)

    def draw(self, surface, only_move=False) -> None:
        if self.smothmove_bool:
            self.pos = Vector2(self.movimiento.update(self.smothmove_pos))
            self.direccion(self.rect)
            self.direccion(self.rect_border)

            if self.mode == 1:
                    self.rect_text.center = self.rect.center
            elif self.mode == 2:
                self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2
                for i, txt in enumerate(self.lista_text):
                    txt.move((self.pos[0],self.pos[1] + self.text_height*i))
            if only_move: return 0

        if self.mode == 2:
            if self.with_rect:
                pag.draw.rect(surface, self.color_rect, self.rect, self.rect_width,self.border_radius
                    , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
                pag.draw.rect(surface, self.border_color, self.rect_border, self.border_width,self.border_radius
                    ,self.border_top_left_radius,self.border_top_right_radius,self.border_bottom_left_radius,self.border_bottom_right_radius)
            for txt in self.lista_text:
                txt.draw(surface)
            return
        
        if self.with_rect:
            pag.draw.rect(surface, self.color_rect, self.rect, self.rect_width,self.border_radius
                , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
            pag.draw.rect(surface, self.border_color, self.rect_border, self.border_width,self.border_radius
                , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
        surface.blit(self.text, self.rect_text)

    def change_text(self, text, font=None) -> None:
        self.lista_text.clear()
        self.raw_text = text
        if font:
            self.raw_font = font
            self.font = pag.font.Font(self.raw_font, self.size)
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
            self.raw_text = text.replace('\t', '    ').split('\n') if '\n' in text else text
            self.text = self.font.render(f'{text[0]}', 1, self.color)
            self.rect_text = self.text.get_rect()
            self.rect = self.text.get_rect()
            self.direccion(self.rect_text)

            for txt in range(len(self.raw_text)):
                self.lista_text.append(Create_text(self.raw_text[txt], self.size, self.raw_font, (self.pos[0],self.pos[1] + self.rect.h*txt), self.dire, self.color, False, self.color_rect, padding=self.padding, rect_width=0))
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
            self.smothmove_pos = Vector2(pos)
        else:
            self.pos = Vector2(pos)
            self.direccion(self.rect)
            self.direccion(self.rect_border)

            if self.mode == 1:
                self.rect_text.center = self.rect.center
            elif self.mode == 2:
                for n, txt in enumerate(self.lista_text):
                    txt.move((self.pos.x,self.pos.y + self.rect.h*n), dire)
                self.direccion(self.rect)
                self.direccion(self.rect_border)
                self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2
    
    def move_rel(self, pos) -> None:
        if self.smothmove_bool:
            self.smothmove_pos = self.smothmove_pos + pos
        else:
            self.pos = Vector2(self.pos + pos)
            self.direccion(self.rect)
            self.direccion(self.rect_border)

    def get_text(self) -> str:
        return self.raw_text

    def __str__(self) -> str:
        return f'{self.raw_text = } - {self.pos = }'

class Create_boton(Create_text):
    '''
    ### More options
     - sound_to_hover
     - sound_to_click
     - toggle_rect
     - color_active
    '''
    def __init__(self, text, size: int, font: str, pos: tuple, padding: int = 20,
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

        self.color_active = kwargs.get('color_active',None)
        self.func = func
    
        self.sound_to_hover = kwargs.get('sound_to_hover',False)
        self.sound_to_click = kwargs.get('sound_to_click',False)

        Create_text.__init__(self,text, size, font, pos, dire, color, with_rect, color_rect, padding=padding, 
                             rect_width=rect_width, border_radius=border_radius,border_top_left_radius=border_top_left_radius, 
                             border_top_right_radius=border_top_right_radius, border_bottom_left_radius=border_bottom_left_radius, 
                             border_bottom_right_radius=border_bottom_right_radius, border_width=border_width,border_color=border_color)
        if self.toggle_rect:
            self.with_rect = False
        self.hover = False

    def draw(self, surface, pos=False) -> None:
        pos = pos if pos else pag.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if not self.hover:
                if self.sound_to_hover:
                    self.sound_to_hover.play()
                self.hover = True
                self.color_rect = self.color_rect_active
                self.change_color(self.color_active) if self.color_active else None
                if self.toggle_rect and self.with_rect2:
                    self.with_rect = True
        else:
            if self.hover:
                self.hover = False
                self.color_rect = self.color_rect_inactive
                self.change_color(self.color_inactive)
                if self.toggle_rect and self.with_rect2:
                    self.with_rect = False
        super().draw(surface)

    def click(self) -> None:
        if self.sound_to_click:
            self.sound_to_click.play()
        if self.func:
            self.func()
    def change_color_ad(self,color,color_active = None) -> None:
        self.color_inactive = color
        self.color_active = color_active if color_active != None else self.color_active
        if self.hover and self.color_active:
            self.change_color(self.color_active)
        else:
            self.change_color(self.color_inactive)

class Input_text(Base):
    def __init__(self, pos: tuple, size: tuple, font: str, text_value: str = 'Type here',max_letter = 20, padding = 20,
        text_color = 'white', background_color = 'black', **kwargs) -> None:
        
        self.border_radius = kwargs.get('border_radius',0)
        self.border_top_left_radius = kwargs.get('border_top_left_radius',-1)
        self.border_bottom_left_radius = kwargs.get('border_bottom_left_radius',-1)
        self.border_top_right_radius = kwargs.get('border_top_right_radius',-1)
        self.border_bottom_right_radius = kwargs.get('border_bottom_right_radius',-1)
        self.border_width = kwargs.get('border_width', -1)
        self.border_color = kwargs.get('border_color', 'black')

        self.size = Vector2(size)
        self.pos = pos
        if isinstance(padding, tuple) or isinstance(padding, Vector2) or isinstance(padding, list):self.padding = Vector2(padding)
        else: self.padding = Vector2(padding,padding)
        self.raw_text = ''
        self.max_letter = max_letter
        self.background_color = background_color


        self.text = Create_text(self.raw_text, size[0], font, pos, 'left', padding=padding)
        self.text_rect = self.text.rect.copy()
        self.text_rect.w = size[1]
        self.create_border(self.text_rect, self.border_width)

        self.text = Create_text(self.raw_text, size[0], font, pos, 'left', padding=5)
        self.text_rect2 = self.text.rect.copy()
        self.text_rect2.w = size[1] - self.padding.x
        self.text_rect2.left += self.padding.x/2
        self.input_surface = pag.surface.Surface(self.text_rect2.size, pag.SRCALPHA)
        self.text = Create_text(self.raw_text, size[0], font, (0,size[0]/2), 'left', text_color, padding=0)


        self.text_value = Create_text(text_value, size[0], font, (0,size[0]/2), 'left', 'gray', padding=0)

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

    def draw(self, surface) -> None:
        if self.backspace and time.time() - self.del_time > .5:
            self.del_letter()
        if self.left_b and time.time() - self.left_time > .5:
            self.left()
        if self.right_b and time.time() - self.right_time > .5:
            self.right()
        pag.draw.rect(surface, self.background_color, self.text_rect, border_radius=self.border_radius)
        pag.draw.rect(surface, self.border_color, self.rect_border, self.border_width,self.border_radius
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
        elif self.raw_text == '': self.text_value.draw(self.input_surface)
        self.text.draw(self.input_surface)
                
        surface.blit(self.input_surface, self.text_rect2)

    def eventos_teclado(self, eventos, offset=False):
        for evento in eventos:
            if self.typing:
                if evento.type == pag.KEYDOWN:
                    if evento.key == pag.K_LEFT:
                        self.left()
                    elif evento.key == pag.K_RIGHT:
                        self.right()
                    elif evento.key == pag.K_BACKSPACE:
                        self.del_letter()
                    elif evento.key == pag.K_RETURN:
                        return "enter"
                elif evento.type == pag.TEXTINPUT:
                    self.add_letter(evento.text)
                elif evento.type == pag.KEYUP:
                    if evento.key == pag.K_BACKSPACE:
                        self.backspace = False
                    elif evento.key == pag.K_LEFT:
                        self.left_b = False
                    elif evento.key == pag.K_RIGHT:
                        self.right_b = False
            if evento.type == pag.MOUSEBUTTONDOWN:
                self.click(evento.pos)

    def click(self, pos) -> None:
        if pos:
            m = Vector2(pos)

        if self.text_rect.collidepoint(m): 
            self.typing = True
        else:
            self.typing = False
            self.backspace = False
            self.typing_line = False
            self.typing_line_time = time.time()
            self.text.change_text(self.raw_text)

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

    def left(self) -> None:
        if not self.left_b:
            self.left_b = True
            self.left_time = time.time()
        self.typing_pos = max(0,self.typing_pos -1)
        self.typing_line = True
        self.typing_line_time = time.time()

    def right(self) -> None:
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
    '''
    ### More options
     - smothscroll
     - with_index
     - padding_top
     - padding_left
    '''
    def __init__(self, size: tuple, pos: tuple, lista: list = None, text_size: int = 20, separation: int = 0,
        selected_color = (100,100,100,100), text_color= 'white', header: bool =False, text_header:str = None,
        background_color = 'black', font=None, **kwargs) -> None:

        self.size = Vector2(size)
        self.pos = Vector2(pos)
        self.text_size = text_size
        self.separation = separation
        self.smothscroll = kwargs.get('smothscroll',True)
        self.background_color = background_color
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.with_index = kwargs.get('with_index',False)
        self.text_color = text_color
        self.header = header
        self.text_header = text_header
        self.font = font

        self.letter_size = Create_text('ssss', self.text_size, self.font, (0,0),padding= separation).rect.height

        self.lista_palabras = ['None', 'None', 'None'] if not lista else lista
        self.lista_objetos: list[Create_text] = []

        if self.header:
            self.text_header: Create_text = Create_text(self.text_header, text_size, None, pos, 'topleft', 'black', True, 'darkgrey',
            padding=(20,15),border_width=1, border_top_left_radius=kwargs.get('header_top_left_radius',20), border_top_right_radius=kwargs.get('header_top_right_radius',20))
            self.text_header.rect.w = size[0]
            self.text_header.rect_border.w = size[0]+1
            self.pos = Vector2(pos[0], pos[1]+self.text_header.rect.h)
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1], size[0], size[1]-self.text_header.rect.h)
        else:
            self.rect = pag.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.lista_surface= pag.surface.Surface(self.rect.size, pag.SRCALPHA)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = pos

        self.desplazamiento = 0
        self.total_height = 0
        self.movimiento = None
        self.smothmove_bool = False
        self.last_mouse_pos = (0,0)

        self.actualizar_lista()
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
        self.select_box = pag.rect.Rect(0,-5000,self.lista_surface_rect.w,self.letter_size)
        self.selected_num = -1

    def draw(self,surface) -> None:
        if self.header:
            self.text_header.draw(surface)
        self.lista_surface.fill(self.background_color)
        pag.draw.rect(self.lista_surface, self.selected_color, self.select_box)
        self.select_box.centery = self.lista_objetos[self.selected_num].rect.centery if self.selected_num != -1 else 4000
        for te in self.lista_objetos:
            te.draw(self.lista_surface, only_move=False if -self.padding_top-30 < te.pos.y < self.rect.h else True)
        if self.scroll:
            self.scroll_func()
            
        if self.total_height + self.lista_surface_rect.h > self.rect.h and self.scroll_bar_active:
            pag.draw.rect(self.lista_surface, 'white', self.barra)
            self.lista_surface.blit(self.bar_surface, self.bar.topleft)

        if self.smothmove_bool:
            self.pos = self.movimiento.update(self.smothmove_pos)
            self.rect.topleft = self.pos

        surface.blit(self.lista_surface,self.rect)

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
            text.move((self.padding_left,(self.letter_size*num) + self.padding_top + self.desplazamiento))

    def actualizar_lista(self) -> None:
        self.lista_objetos.clear()
        for num ,text in enumerate(self.lista_palabras):
            self.lista_objetos.append(Create_text(text, self.text_size, self.font, (self.padding_left,(self.letter_size*num) + self.padding_top), 'topleft', self.text_color, padding=20))
        
        self.total_height = 0
        if self.smothscroll:
            for x in self.lista_objetos:
                x.smothmove(60, 1.5, 1, 1.5)
        self.total_height = self.lista_objetos[-1].rect.bottom - self.lista_surface_rect.h

    def append(self,texto:str) -> None:
        self.lista_palabras.append(texto)
        self.actualizar_lista()

    def change_list(self, lista: list) -> None:
        self.lista_palabras: list[str] = [] if not lista else lista
        if self.scroll_bar_active:
            self.select_box.top = self.rect.bottom
        self.selected_num = -1
        self.actualizar_lista()
    
    def clear(self) -> None:
        self.lista_palabras.clear()
        self.selected_num = -1

    def click(self,pos):
        m = Vector2(pos)
        m -= self.pos
        if self.header: m += (0,10)
        if self.scroll_bar_active and self.barra.collidepoint(m-(0,10)):
            self.scroll = True
            self.last_mouse_pos = pag.mouse.get_pos()
            return 'scrolling'
        for index, te in enumerate(self.lista_objetos):
            if te.pos.y < m.y < te.pos.y+te.rect.h:
                self.select_box.centery = te.rect.centery
                self.select(index, False)
                return {'index': index,'text': te.get_text()}

    def select(self, index: int = -2000, driff = True) -> str:
        if index != -2000:
            self.select_box.centery = self.lista_objetos[index].rect.centery
            self.selected_num=index
            if driff:
                self.desplazamiento = (-self.letter_size*index + self.padding_top) + self.lista_surface_rect.h/2
            self.rodar(0)
            return {'text': self.lista_objetos[index].raw_text, 'index': index}
        
        self.select_box.top = self.lista_surface_rect.h
        self.selected_num=-1
        return False

    def scroll_func(self) -> None:
        
        var = Vector2(pag.mouse.get_pos())
        m_pos = self.last_mouse_pos - var
        m_pos.y *= -1
        self.last_mouse_pos = var

        self.barra.centery += m_pos.y
        self.desplazamiento = -self.total_height *(self.barra.top / (self.lista_surface_rect.h-self.barra.h))

        if self.desplazamiento > 0:
            self.desplazamiento = self.padding_top
            self.barra.top = 0
        elif self.desplazamiento < -self.total_height:
            self.desplazamiento = -self.total_height
            self.barra.bottom = self.rect.h

        for num ,text in enumerate(self.lista_objetos):
            text.move((self.padding_left,self.letter_size*num + self.desplazamiento))
        
    def get_list(self) -> list[str]:
        return self.lista_palabras
    
    def __getitem__(self,index):
        return self.lista_palabras[index]
    
    def __setitem__(self,index,value):
        self.lista_palabras[index] = value
        self.actualizar_lista()
    def __repr__(self):
        return self.lista_palabras
    def __str__(self) -> str:
        text = f'{'_':_>20}\n'
        text += '\n'.join(self.lista_palabras)
        text += f'\n{'-':-^20}\n'
        return text

class Multi_list(Base):
    '''
    ### More options
     - smothscroll
     - with_index
     - padding_top
     - padding_left
    '''
    def __init__(self, size:tuple,pos:tuple,num_lists:int=2,lista: list[list] = None, text_size: int = 20, separation: int = 0,
        background_color = 'black', selected_color = (100,100,100,100), text_color= 'white', colums_witdh= -1, header: bool =True,
        header_text: list = None, dire: str = 'topleft', fonts=None, default: list[list]=None, **kwargs) -> None:
        
        self.size = Vector2(size)
        self.pos = Vector2(pos)
        self.default = [None for _ in range(num_lists)] if not default else default
        self.lista_palabras = self.default if not lista else lista
        self.text_size = text_size
        self.separation = separation
        self.smothscroll = kwargs.get('smothscroll',True)
        self.background_color = background_color
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.with_index = kwargs.get('with_index',False)
        self.text_color = text_color
        if num_lists <= 0: raise Exception('\n\nComo vas a hacer 0 listas en una multilista\nPensá bro...')
        self.num_list = num_lists
        self.colums_witdh = [(self.size[0]/self.num_lists)*x for x in range(self.num_list)] if colums_witdh == -1 else list(colums_witdh)
        self.colums_witdh.append(1)
        self.header = header
        self.text_header = [None for x in range(num_lists)] if header_text == None else header_text
        self.fonts = [None for x in range(num_lists)] if fonts == None else fonts
        self.header_radius = kwargs.get('header_radius',0)
        self.border_color = kwargs.get('border_color', 'black')
        self.dire = dire

        self.listas: list[List_Box] = []
        self.lineas = []
        self.scroll = False
        self.smothmove_bool = False
        self.actual_index = -1

        self.rect = pag.rect.Rect(pos[0], pos[1], size[0], size[1])
        self.direccion(self.rect)
        self.lista_surface= pag.surface.Surface(self.rect.size, pag.SRCALPHA)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = self.pos
        for x in range(num_lists):
            self.lineas.append([((self.size.x*self.colums_witdh[x] -1),0 if not self.header else -20), ((self.size.x*self.colums_witdh[x] -1),self.rect.h)])
            separar = Create_text('Hola', self.text_size, self.fonts[-1], (0,0)).rect.h
            separar = separar - Create_text('Hola', self.text_size, self.fonts[0], (0,0)).rect.h
            self.listas.append(List_Box(((self.size.x*self.colums_witdh[x+1]) - (self.size.x*self.colums_witdh[x]), self.size.y), 
                (self.size.x*self.colums_witdh[x],0), [self.lista_palabras[x]], self.text_size, self.separation+(separar if x != num_lists-1 else 0), 
                self.selected_color, self.text_color, background_color=(0,0,0,0), smothscroll=self.smothscroll, 
                padding_top=self.padding_top-(separar//2 if x == num_lists-1 else 0), padding_left=self.padding_left, 
                with_index=self.with_index if x == 0 and self.with_index else False, 
                scroll_bar_active=False if x != num_lists-1 else True,
                header=True, text_header=self.text_header[x], header_top_left_radius=20 if x == 0 else 0, 
                header_top_right_radius=20 if x == self.num_list-1 else 0, font=self.fonts[x]))


    def draw(self,surface) -> None:
        if self.smothmove_bool:
            self.pos = self.movimiento.update(self.smothmove_pos)
            self.direccion(self.rect)

        self.lista_surface.fill(self.background_color)
        if self.header:
            pag.draw.rect(self.lista_surface, (0,0,0,0), pag.rect.Rect(0,0,self.rect.w, 20))
        for x in self.listas:
            x.draw(self.lista_surface)
        if self.scroll:
            for x in self.listas:
                x.desplazamiento = self.listas[-1].desplazamiento
                x.selected_num = self.listas[-1].selected_num
                x.rodar(0)
        for line in self.lineas[1:]:
            pag.draw.line(self.lista_surface, self.border_color, line[0], line[1], 2)
        for x in self.listas:
            pag.draw.rect(self.lista_surface, self.border_color, x.rect, 1)
        surface.blit(self.lista_surface,self.rect)

    def move(self, pos) -> None:
        if self.smothmove_bool:
            self.smothmove_pos = pos
        else:
            self.pos = Vector2(*pos)
            self.direccion(self.rect)

    def move_rel(self, pos) -> None:
        if self.smothmove_bool:
            self.smothmove_pos = self.smothmove_pos + pos
        else:
            self.pos = Vector2(self.pos + pos)
            self.direccion(self.rect)

    def rodar(self,y) -> None:
        for x in self.listas:
            x.rodar(y)

    def append(self,data) -> None:
        # for i,x in enumerate(data):
        #     self.listas[i].append(x)
        for i in range(self.num_list):
            if i < len(data):
                self.listas[i].append(data[i])
            else:
                self.listas[i].append(self.default[i])

    def change_list(self, list: list) -> None:
        self.clear()
        for x in list:
            self.append(x)

    def clear(self) -> None:
        [x.clear() for x in self.listas]

    def click(self,pos):
        m = Vector2(pos)
        m -= self.pos
        for i,x in sorted(enumerate(self.listas),reverse=True):
            a = x.click(m)
            if a == 'scrolling':
                self.scroll = True
            elif isinstance(a,dict):
                minilista = [l.select(a['index'], False)['text'] for l in self.listas]
                return minilista


    def select(self, index: int = -2000) -> str:
        for i,x in sorted(enumerate(self.listas),reverse=True):
            a = x.select(index=index)
            minilista = [l.select(index=int(a['index']))['text'] for l in self.listas]
            return minilista

    def detener_scroll(self) -> None:
        self.scroll = False
        for x in self.listas:
            x.scroll = False

    def get_list(self) -> list:
        var1 = [x.get_list() for x in self.listas]
        return list([list(x) for x in zip(*var1)])

    def __getitem__(self,index: int):
        # return [li[index] for li in self.listas]
        return self.listas[index]
    def __setitem__(self,index,value):
        self.listas[index] = value