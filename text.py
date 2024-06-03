import pygame as pag, time
from pygame.math import Vector2
from typing import Literal
from .obj_Base import Base


'''
1) Hacer superficies y normalizar una funcion draw.
4) Hacer otra clase multilista, donde las listas sean tuplas y no List_box.
'''

class Create_text(Base):
    """
    # Funciones

    ### Comandos
    - draw() - Dibuja el texto\n
        - Si colocas border radius -1 sera redondo\n
    - change_text() - Cambia el texto\n
    - change_color() - Cambia el color del texto\n
    - get_text() - Retorna el texto actual
    - move() - Mueve el texto al sitio seleccionado\n
    - smothmove() - permite una transicion suave en el movimiento utilizando la clase Second Order Dinamics
    """
    
    def __init__(self,text: str,size: int,font: str, pos: tuple,
                 dire: Literal["center","left","right","topleft","topright","bottomleft","bottomright"] ='center',
                 color='white',with_rect = False, color_rect ='black', border_width = -1, padding: int|list|tuple = 20, 
                 width = 0, height = 0, rect_width= 0, **kwargs) -> None:
        super().__init__(pos,dire)
        pag.font.init()
        text = str(text)
        self.raw_text = text.replace('\t', '    ').split('\n') if '\n' in text else text
        self.__size = size
        self.raw_font = font
        self.__color = color
        self.with_rect = with_rect
        self.color_rect = color_rect
        self.padding: Vector2 = Vector2(padding)
        self.rect_width = rect_width
        self.default_width = width
        self.default_height = height
        self.__width = width
        self.__height = height
        
        self.border_radius = kwargs.get('border_radius',0)
        self.border_top_left_radius = kwargs.get('border_top_left_radius',-1)
        self.border_bottom_left_radius = kwargs.get('border_bottom_left_radius',-1)
        self.border_top_right_radius = kwargs.get('border_top_right_radius',-1)
        self.border_bottom_right_radius = kwargs.get('border_bottom_right_radius',-1)
        self.border_width = border_width
        self.border_color = kwargs.get('border_color', 'black')

        self.lista_text: Create_text = []
        self.mode = 1
        self.__font = pag.font.Font(self.raw_font, size)

        self.smothmove_bool = False

        self.__generate()
    
    def __generate(self):
        self.raw_text = self.text.replace('\t', '    ').split('\n') if '\n' in self.raw_text else self.raw_text
        self.__width = self.default_width
        self.__height = self.default_height
        if not isinstance(self.raw_text, list):
            self.mode = 1

            self.text_surf = self.__font.render(f'{self.raw_text}', 1, self.__color)
            self.rect = self.text_surf.get_rect()
            self.rect_text = self.text_surf.get_rect()
            if self.border_radius == -1:
                self.border_radius = 100_000
                n = max(self.rect.h + self.padding.y*2,self.rect.w + self.padding.x*2,self.__width,self.__height)
                self.rect.size = (n, n)
            else:
                self.rect.size = (max(self.__width,self.rect.w + self.padding.x), max(self.__height,self.rect.h + self.padding.y))
            self.direccion(self.rect)
            self.rect_text.center = self.rect.center
            self.create_border(self.rect, self.border_width)
        else:
            self.mode = 2
            self.lista_text.clear()

            self.text_surf = self.__font.render(f'{self.raw_text[0]}', 1, self.__color)
            self.text_lines = len(self.raw_text)
            self.text_height = self.text_surf.get_rect().h
            self.rect_text = self.text_surf.get_rect()
            self.rect = self.text_surf.get_rect()

            for txt in range(len(self.raw_text)):
                self.lista_text.append(Create_text(self.raw_text[txt], self.__size, self.raw_font, (self.pos[0],self.pos[1] + self.rect.h*txt), self.dire, self.color, False, self.color_rect, padding=self.padding, rect_width=0))
            
            if self.border_radius == -1:
                self.border_radius = 100_000
                self.rect.size = (max(self.rect.h * len(self.raw_text) + self.padding[0],max(self.__font.render(txt, 1, self.__color).get_rect().width + self.padding[0] for txt in self.raw_text)), max(self.rect.h * len(self.raw_text) + self.padding[2],max(self.__font.render(tixt, 1, self.color).get_rect().width + self.padding[1] for tixt in self.raw_text)))
            else:
                self.rect.width = min(max(self.__font.render(tixt, 1, self.__color).get_rect().width * 1.2 for tixt in self.raw_text), max(self.__font.render(tixt, 1, self.color).get_rect().width + self.padding[0] for tixt in self.raw_text))
                self.rect.height = (self.text_height * (len(self.raw_text)-1)) + self.padding[0]

            self.direccion(self.rect)
            self.rect.centery = self.rect_text.centery + (self.text_height * (len(self.raw_text)-1))/2
            
            self.create_border(self.rect, self.border_width)
        self.__width = self.rect.w
        self.__height = self.rect.h

    @property
    def text(self):
        return self.raw_text
    @text.setter
    def text(self,texto):
        self.raw_text = str(texto)
        self.__generate()
    @property
    def font(self):
        return self.__font
    @font.setter
    def font(self,font):
        self.raw_font = font
        self.__font = pag.font.Font(self.raw_font, self.size)
        self.__generate()
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self,size):
        self.__size = size
        self.__font = pag.font.Font(self.raw_font, self.__size)
        self.__generate()
    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self,color):
        self.__color = color
        if self.mode == 1:
            self.text_surf = self.font.render(f'{self.raw_text}', 1, self.color)
        elif self.mode == 2:
            for txt in self.lista_text:
                txt.color = color
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self,width):
        self.__width = max(width,self.rect_text.w + self.padding[0]*2)
        self.rect.width = self.width
        self.create_border(self.rect,self.border_width)
        self.direccion(self.rect)
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self,height):
        self.__height = max(height,self.rect_text.h + self.padding[1]*2)
        self.rect.height = self.height
        self.create_border(self.rect,self.border_width)
        self.direccion(self.rect)

    def update(self, pos = None):
        super().update(pos)

        self.direccion(self.rect)

        if self.mode == 1:
            self.rect_text.center = self.rect.center
        elif self.mode == 2:
            self.rect.centery = self.rect_text.centery + (self.rect_text.h * (len(self.raw_text)-1))/2
            for i, txt in enumerate(self.lista_text):
                txt.pos = (self.pos[0],self.pos[1] + self.text_height*i)

    def draw(self, surface, only_move=False) -> None:
        # if self.smothmove_bool:
        # self.update()
        self.rect_text.center = self.rect.center
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

        surface.blit(self.text_surf, self.rect_text)

    def __str__(self) -> str:
        return f'{self.raw_text = } - {self.pos = }'

class Create_boton(Create_text):
    '''
    ### More options
     - sound_to_hover: pag.Sound
     - sound_to_click: pag.Sound
     - toggle_rect: bool
     - color_active: pygame.Color
     - color_rect_active: pygame.Color
    '''
    def __init__(self, text, size: int, font: str, pos: tuple, padding: int|list|tuple = 20,
        dire: Literal["center","left","right","top","bottom","topleft","topright","bottomleft","bottomright"] = 'center', color = 'black', color_rect = 'darkgrey',
        color_rect_active='lightgrey',rect_width=0,border_radius:int=15,border_top_left_radius:int=-1,
        border_top_right_radius: int = -1, border_bottom_left_radius: int = -1,
        border_bottom_right_radius: int = -1, border_width = 2, border_color = 'black', with_rect = True,
        func = None, width = 0, height = 0, **kwargs) -> None:

        self.color_rect_active = color_rect_active if color_rect_active != None else color_rect
        self.color_rect_inactive = color_rect
        self.color_inactive = color
        self.with_rect2 = with_rect

        self.toggle_rect = kwargs.get('toggle_rect',False)
        self.border_color_inactive = border_color
        self.color_border_active = kwargs.get('color_border_active',border_color)

        self.color_active = kwargs.get('color_active',None)
        self.func = func
    
        self.sound_to_hover = kwargs.get('sound_to_hover',False)
        self.sound_to_click = kwargs.get('sound_to_click',False)

        Create_text.__init__(self,text, size, font, pos, dire, color, with_rect, color_rect, padding=padding, 
                             rect_width=rect_width, border_radius=border_radius,border_top_left_radius=border_top_left_radius, 
                             border_top_right_radius=border_top_right_radius, border_bottom_left_radius=border_bottom_left_radius, 
                             border_bottom_right_radius=border_bottom_right_radius, border_width=border_width,border_color=border_color,
                             width = width, height = height)
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
                self.color = self.color_active if self.color_active else self.color_inactive
                self.border_color = self.color_border_active
                if self.toggle_rect and self.with_rect2:
                    self.with_rect = True
        else:
            if self.hover:
                self.hover = False
                self.color_rect = self.color_rect_inactive
                self.color = self.color_inactive
                self.border_color = self.border_color_inactive
                if self.toggle_rect and self.with_rect2:
                    self.with_rect = False
        super().draw(surface)

    def click(self,pos) -> bool:
        if not self.rect.collidepoint(pos):
            return False
        if self.sound_to_click:
            self.sound_to_click.play()
        if self.func:
            self.func()
        return True
    def change_color_ad(self,color,color_active = None) -> None:
        self.color_inactive = color
        self.color_active = color_active if color_active != None else self.color_active
        if self.hover and self.color_active:
            self.color = self.color_active
        else:
            self.color = self.color_inactive
    def change_color_rect_ad(self,color_inactive,color_active = None) -> None:
        self.color_rect_inactive = color_inactive if color_inactive != None else self.color_rect_inactive
        self.color_rect_active = color_active if color_active != None else self.color_rect_active
        if self.hover:
            self.color_rect = self.color_rect_active
        else:
            self.color_rect = self.color_rect_inactive

class Input_text(Base):
    '''
    for x in self.lista_inputs:
        x.eventos_teclado(eventos)
    '''
    def __init__(self, pos: tuple, text_size: int, font: str, text_value: str = 'Type here',max_letter = 20, padding = 20,
        width=100, height=50, text_color='white',text_value_color='grey', background_color = 'black', dire: str = 'topleft', **kwargs) -> None:
        
        super().__init__(pos,dire)
        self.border_radius = kwargs.get('border_radius',0)
        self.border_top_left_radius = kwargs.get('border_top_left_radius',-1)
        self.border_bottom_left_radius = kwargs.get('border_bottom_left_radius',-1)
        self.border_top_right_radius = kwargs.get('border_top_right_radius',-1)
        self.border_bottom_right_radius = kwargs.get('border_bottom_right_radius',-1)
        self.border_width = kwargs.get('border_width', -1)
        self.border_color = kwargs.get('border_color', 'black')
        self.pointer_color = kwargs.get('pointer_color', 'white')

        self.text_size = text_size
        self.text_color = text_color
        self.text_value_color = text_value_color

        self.padding = Vector2(padding)
        self.raw_text = ''
        self.text_value = text_value
        self.max_letter = max_letter
        self.background_color = background_color
        self.font = font
        
        self.width = width
        self.height = height
        self.generate()

        self.typing = False
        self.typing_pos = 0
        self.backspace = False
        self.supr = False
        self.del_time = 0
        self.left_b = False
        self.left_time = 0
        self.right_b = False
        self.right_time = 0
        self.typing_line = False
        self.typing_line_time = time.time()
        self.letter_pos = [0]
        self.button_pressed_time = 0
        self.draw_surf()

    def generate(self):
        t = Create_text('', self.text_size, self.font, self.pos, 'left', padding=self.padding,width=self.width,height=self.height)
        self.rect = t.rect.copy()

        self.text = Create_text('abdc123--||', self.text_size, self.font, self.pos, 'left',self.text_color,True, self.background_color,width=self.width-self.padding.x*2, padding=5)
        self.rect2 = self.text.rect.copy()
        self.input_surface = pag.Surface(self.rect2.size)
        self.input_surface.fill(self.background_color)
        self.surf_rect = self.input_surface.get_rect()

        self.text = Create_text(self.raw_text, self.text_size, self.font, (0,self.input_surface.get_height()/2), 'left',self.text_color,True, self.background_color, padding=0)
        self.text_value = Create_text(self.text_value, self.text_size, self.font, (0,self.input_surface.get_height()/2), 'left',self.text_value_color,True, self.background_color, padding=0)

        self.surf_rect.center = self.rect.center
        # self.width = self.rect.w
        self.create_border(self.rect, self.border_width)
        self.direccion(self.rect)


    def draw_surf(self):
        self.input_surface.fill(self.background_color)
        if self.raw_text == '':
            self.text_value.draw(self.input_surface)
        else:
            self.text.draw(self.input_surface)
        if self.typing_line:
            pag.draw.line(self.input_surface, self.pointer_color, (sum(self.letter_pos[:self.typing_pos])+self.text.left,0),(sum(self.letter_pos[:self.typing_pos])+self.text.left,self.input_surface.get_height()))


    def draw(self, surface) -> None:
        if time.time() - self.button_pressed_time > .5:
            if self.backspace and time.time() - self.del_time > .03:
                self.del_letter()
                self.del_time = time.time()
            elif self.left_b and time.time() - self.left_time > .03:
                self.to_left()
                self.left_time = time.time()
            elif self.right_b and time.time() - self.right_time > .03:
                self.to_right()
                self.right_time = time.time()
            self.draw_surf()
        pag.draw.rect(surface, self.background_color, self.rect, 0, self.border_radius, self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
        pag.draw.rect(surface, self.border_color, self.rect_border, self.border_width,self.border_radius
            , self.border_top_left_radius, self.border_top_right_radius, self.border_bottom_left_radius, self.border_bottom_right_radius)
    
        if self.typing:
            if time.time()-self.typing_line_time > .7:
                self.typing_line = not self.typing_line
                self.typing_line_time = time.time()
                self.draw_surf()
        self.surf_rect.center = self.rect.center
        surface.blit(self.input_surface, self.surf_rect)

    def eventos_teclado(self, eventos):
        for evento in eventos:
            if self.typing:
                if evento.type == pag.KEYDOWN and not (self.backspace or self.left_b or self.right_b):
                    if evento.key == pag.K_LEFT:
                        self.to_left()
                    elif evento.key == pag.K_RIGHT:
                        self.to_right()
                    elif evento.key == pag.K_BACKSPACE:
                        self.del_letter()
                    # elif evento.key == pag.K_DELETE:
                    #     self.del_letter()
                    elif evento.key == pag.K_RETURN:
                        return "enter"
                    self.button_pressed_time = time.time()
                elif evento.type == pag.TEXTINPUT:
                    self.add_letter(evento.text)
                    self.draw_surf()
                elif evento.type == pag.KEYUP:
                    if evento.key == pag.K_BACKSPACE:
                        self.backspace = False
                    elif evento.key == pag.K_LEFT:
                        self.left_b = False
                    elif evento.key == pag.K_RIGHT:
                        self.right_b = False
            if evento.type == pag.MOUSEBUTTONDOWN and evento.button == 1:
                self.click(evento.pos)

    def check_pos_letter_click(self,x):
        acumulacion = 0
        for pos, i in enumerate(self.letter_pos):
            if x < acumulacion+self.text.rect_text.left:
                return pos
            acumulacion += i
        else:
            return len(self.raw_text)

    def click(self, pos) -> None:

        if self.rect.collidepoint(pos): 
            self.typing = True
            if 'left' in self.dire:
                neg = self.pos.x
            elif 'center' in self.dire:
                neg = self.pos.x - self.rect.w/2
            elif 'right' in self.dire:
                neg = self.pos.x + self.rect.w/2
            self.typing_pos = self.check_pos_letter_click(pos[0]-neg-(self.padding.x)-self.text_size/3)
            self.typing_line = True
            self.typing_line_time = time.time()
        else:
            self.typing = False
            self.backspace = False
            self.typing_line = False
            self.typing_line_time = time.time()
            self.text.text = self.raw_text
        self.draw_surf()

    def add_letter(self, t) -> None:
        if len(self.raw_text) < self.max_letter:
            self.raw_text = self.raw_text[:self.typing_pos] + t + self.raw_text[self.typing_pos:]
            self.text.text = self.raw_text
            self.letter_pos.insert(self.typing_pos,Create_text(t,self.text_size, self.font, (0,0), padding=0).rect.w)
            self.typing_pos += 1
            suma = sum(self.letter_pos[:self.typing_pos])
            if suma > self.rect2.w-5:
                self.text.pos = (self.rect2.w-2,self.input_surface.get_height()/2)
                self.text.dire = 'right'
            elif suma + self.text.left < self.rect2.w:
                self.text.pos = (0,self.input_surface.get_height()/2)
                self.text.dire = 'left'
        self.typing_line = True
        self.typing_line_time = time.time()

    def to_left(self) -> None:
        if not self.left_b:
            self.left_b = True
            self.left_time = time.time()
        self.typing_pos = max(0,self.typing_pos -1)
        self.typing_line = True
        self.typing_line_time = time.time()
        suma = sum(self.letter_pos[:self.typing_pos])
        # if suma > self.rect2.w-5:
        #     self.text.pos = (self.rect2.w-2,self.input_surface.get_height()/2)
        #     self.text.dire = 'right'
        if self.text.left+self.letter_pos[self.typing_pos-1] > 0:
            self.text.pos = (0,self.input_surface.get_height()/2)
            self.text.dire = 'left'
        elif suma + self.text.left < self.rect2.w/10:
            self.text.pos += (self.letter_pos[self.typing_pos-1],0)
        self.draw_surf()

    def to_right(self) -> None:
        if not self.right_b:
            self.right_b = True
            self.right_time = time.time()
        self.typing_pos = min(len(self.raw_text),self.typing_pos + 1)
        self.typing_line = True
        self.typing_line_time = time.time()
        suma = sum(self.letter_pos[:self.typing_pos])
        suma_neg = sum(self.letter_pos[self.typing_pos:])
        # if suma_neg < self.rect2.w*.2:
        if suma > self.rect2.w*.9:
            self.text.pos -= (self.letter_pos[self.typing_pos],0)
        if self.text.width>self.rect2.w and suma_neg < self.rect2.w*.2:
            self.text.pos = (self.rect2.w-1,self.input_surface.get_height()/2)
            self.text.dire = 'right'
        self.draw_surf()

    def del_letter(self) -> None:
        if not self.backspace:
            self.backspace = True
            self.del_time = time.time()
        if len(str(self.raw_text)) > 0:
            if self.typing_pos == 0:
                return
            
            self.raw_text = self.raw_text[:self.typing_pos-1] + self.raw_text[self.typing_pos:]
            self.letter_pos.pop(self.typing_pos)
            self.typing_pos -= 1
            self.text.text = self.raw_text
            suma = sum(self.letter_pos[:self.typing_pos])
            if suma > self.rect2.w-5:
                self.text.pos = (self.rect2.w-2,self.input_surface.get_height()/2)
                self.text.dire = 'right'
            elif suma + self.text.left < self.rect2.w:
                self.text.pos = (0,self.input_surface.get_height()/2)
                self.text.dire = 'left'
        self.typing_line = True
        self.typing_line_time = time.time()
        self.draw_surf()

    def clear(self):
        self.letter_pos = [0]
        self.raw_text = ''
        self.typing_pos = 0
        self.typing_line = False
        self.typing_line_time = time.time()
        self.text.text = self.raw_text
        self.text.pos = (0,self.input_surface.get_height()/2)
        self.text.dire = 'left'
        self.draw_surf()


    def set(self, text) -> None:
        'Cambiar el texto'
        self.clear()
        for x in f'{text}':
            self.add_letter(x)
        self.draw_surf()

    def get_text(self) -> str:
        return self.raw_text
    
    def __str__(self) -> str:
        return self.raw_text

class List_Box(Base):
    '''
    ### More options
     - smothscroll
     - with_index
     - padding_top
     - padding_left

    ## Ejemplo Codigo:
    
    elif evento.type == MOUSEMOTION and [lista].scroll:
        [lista].rodar_mouse(evento.rel[1])
    '''
    def __init__(self, size: tuple, pos: tuple, lista: list = None, text_size: int = 20, separation: int = 0,
        selected_color = (100,100,100,100), text_color= 'white', header: bool =False, text_header:str = None,
        background_color = 'black', font=None, smothscroll=False, dire='topleft', **kwargs) -> None:

        super().__init__(pos,dire)
        self.size = Vector2(size)
        self.__width = size[0]
        self.__height = size[1]
        self.text_size = text_size
        self.separation = separation
        self.__smothscroll = smothscroll
        self.background_color = background_color
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.with_index = kwargs.get('with_index',False)
        self.text_color = text_color
        self.header = header
        self.text_header = text_header
        self.font = font

        self.header_top_right_radius = kwargs.get('header_top_right_radius',20)
        self.header_top_left_radius = kwargs.get('header_top_left_radius',20)
        self.header_border_color = kwargs.get('header_border_color',20)
        self.scroll_bar_active = kwargs.get('scroll_bar_active',True)

        self.letter_size = Create_text('ssss|', self.text_size, self.font, (0,0),padding= separation).rect.height

        self.lista_palabras = ['None', 'None', 'None'] if not lista else lista
        self.lista_objetos: list[Create_text] = []
        
        self.desplazamiento = 0
        self.total_height = 0
        self.movimiento = None
        self.smothmove_bool = False
        self.last_mouse_pos = (0,0)

        self.__generate()
    
    def __generate(self):

        if self.header:
            self.text_header: Create_text = Create_text(self.text_header, 23, None, self.pos, 'bottomleft', 'black', True, 'darkgrey',
            padding=(5,15),border_width=1, border_top_left_radius=self.header_top_left_radius,
            border_top_right_radius=self.header_top_right_radius, border_color=self.header_border_color, width=self.size[0])
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1]+self.text_header.rect.h, self.size[0], self.size[1]-self.text_header.rect.h)
        else:
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.lista_surface= pag.surface.Surface(self.rect.size)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = self.pos
        self.lista_surface.fill((254,1,1))
        self.lista_surface.set_colorkey((254,1,1))


        self.actualizar_lista()

        #La barra que sube y baja
        self.bar_height = max(10,self.lista_surface_rect.h*(self.lista_surface_rect.h/self.lista_objetos[-1].rect.bottom))
        self.barra = pag.rect.Rect(self.lista_surface_rect.w - 10, 0, 10, self.bar_height)
        self.scroll = False

        #cuadro de seleccion
        self.select_box = pag.rect.Rect(0,-5000,self.lista_surface_rect.w,self.letter_size)
        self.selected_num = -1
        self.draw_surf()

    def draw_surf(self):
        self.lista_surface.fill(self.background_color)
        pag.draw.rect(self.lista_surface, self.selected_color, self.select_box)
        for te in self.lista_objetos:
            te.update()
        #     te.draw(self.lista_surface, only_move=False if -self.padding_top-30 < te.raw_pos.y < self.rect.h else True)

        self.lista_surface.blits([(te.text_surf,te.rect_text) for te in self.lista_objetos])
            
        if self.scroll_bar_active and self.total_height + self.lista_surface_rect.h > self.rect.h:
            pag.draw.rect(self.lista_surface, 'white', self.barra,border_radius=5)

    def draw(self,surface) -> None:
        if self.header:
            self.text_header.draw(surface)

        if self.smothmove_bool:
            self.update()
            
        if self.smothscroll and self.selected_num >= 0:
            self.select_box.centery = self.lista_objetos[self.selected_num].centery
        else:
            self.select_box.centery = -100
        if self.smothscroll:
            self.draw_surf()

        surface.blit(self.lista_surface,self.rect)
    
    def actualizar_lista(self) -> None:
        self.lista_objetos.clear()
        for num ,text in enumerate(self.lista_palabras):
            self.lista_objetos.append(Create_text(text, self.text_size, self.font, (self.padding_left,(self.letter_size*num) + self.padding_top), 'topleft', self.text_color, padding=20))
        
        self.total_height = 0
        if self.smothscroll:
            for x in self.lista_objetos:
                x.smothmove(60, 1.4, 1, 1.5)
                # x.simple_acceleration_move(2)
        self.total_height = self.lista_objetos[-1].rect.bottom - self.lista_surface_rect.h
        self.bar_height = max(10,self.lista_surface_rect.h*(self.lista_surface_rect.h/self.lista_objetos[-1].rect.bottom))
        self.barra = pag.rect.Rect(self.lista_surface_rect.w - 10, 0, 10, self.bar_height)
        self.selected_num = -1

    def append(self,texto:str) -> None:
        self.selected_num = -1
        self.lista_palabras.append(str(texto))
        self.lista_objetos.append(Create_text(texto, self.text_size, self.font, (self.padding_left,(self.letter_size*(len(self.lista_palabras)-1)) + self.padding_top), 'topleft', self.text_color, padding=20))
        if self.smothscroll:
            self.lista_objetos[-1].smothmove(60, 1.5, 1, 1.5)
            # self.lista_objetos[-1].simple_acceleration_move(2)
        self.total_height = self.lista_objetos[-1].rect.bottom - self.lista_surface_rect.h
        self.bar_height = max(10,self.lista_surface_rect.h*(self.lista_surface_rect.h/self.lista_objetos[-1].rect.bottom))
        self.barra = pag.rect.Rect(self.lista_surface_rect.w - 10, 0, 10, self.bar_height)
        self.rodar(0)
        if not self.smothscroll:
            self.draw_surf()
    def change_list(self, lista: list) -> None:
        self.selected_num = -1
        self.select_box.centery = -100
        self.draw_surf()
        self.lista_palabras: list[str] = [] if not lista else lista
        self.select_box.top = self.rect.bottom
        self.actualizar_lista()
        if not self.smothscroll:
            self.draw_surf()
    
    def clear(self) -> None:
        self.selected_num = -1
        self.lista_palabras.clear()
        self.lista_objetos.clear()
        if not self.smothscroll:
            self.draw_surf()

    def click(self,pos):
        m = Vector2(pos)
        m -= self.pos
        # m -= (0,self.text_header.height)
        if self.header: m += (0,5)
        if self.scroll_bar_active and self.barra.collidepoint(m): # -(0,10) 
            self.scroll = True
            self.last_mouse_pos = pag.mouse.get_pos()
            return 'scrolling'
        for index, te in enumerate(self.lista_objetos):
            if te.pos.y < m.y < te.pos.y+te.rect.h:
                self.select_box.centery = te.rect.centery
                self.select(index, False)
                return {'index': index,'text': te.text}
        self.select(-2000)
    def select(self, index: int = -2000, driff = True) -> dict|bool:
        if index != -2000:
            self.select_box.centery = self.lista_objetos[index].rect.centery
            self.selected_num=index
            if driff:
                self.desplazamiento = (-self.letter_size*index + self.padding_top) + self.lista_surface_rect.h/2
            self.rodar(0)
            return {'text': self.lista_objetos[index].raw_text, 'index': index}
        
        self.select_box.top = self.lista_surface_rect.h
        self.selected_num=-1
        if not self.smothscroll:
            self.draw_surf()
        return False

    def rodar(self,y) -> None:
        if self.total_height + self.lista_surface_rect.h < self.rect.h:
            return

        self.desplazamiento += y
        if self.desplazamiento > 0:
            self.desplazamiento = 0
            if self.scroll_bar_active:
                self.barra.top = 0
        elif self.desplazamiento < -self.total_height:
            self.desplazamiento = -self.total_height
            if self.scroll_bar_active:
                self.barra.bottom = self.rect.h
                
        if self.scroll_bar_active and self.total_height>0:
            self.barra.top = -(self.lista_surface_rect.h-self.barra.h) * (self.desplazamiento/self.total_height)
        else:
            self.barra.top = 0

        for num ,text in enumerate(self.lista_objetos):
            text.pos = (self.padding_left,(self.letter_size*num) + self.padding_top + self.desplazamiento)
        if self.selected_num >= 0:
            self.select_box.centery = self.lista_objetos[self.selected_num].centery
        else:
            self.select_box.centery = -400

        if not self.smothscroll:
            self.draw_surf()
    def rodar_mouse(self,rel):
        self.barra.centery += rel
        if self.barra.top <= 0:
            self.barra.top = 0
            self.desplazamiento = 0
            self.rodar(0)
            return
        self.desplazamiento = -(self.total_height/((self.lista_surface_rect.h-self.barra.h)/self.barra.top))
        self.rodar(0)

    def get_list(self) -> list[str]:
        return self.lista_palabras
    
    def resize(self, size):
        self.__width = max(size[0],10)
        self.__height = max(size[1],5)
        self.size = Vector2(self.__width,self.__height)
        if self.header:
            # self.text_header.width = self.size.x
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1]+self.text_header.height, self.size[0], self.size[1]-self.text_header.rect.h)
            self.text_header.bottomleft = self.pos
            self.text_header.width = self.size[0]
        else:
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            
        self.lista_surface= pag.surface.Surface(self.rect.size)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = self.pos
        self.lista_surface.fill((254,1,1))
        self.lista_surface.set_colorkey((254,1,1))
        
        self.select_box = pag.rect.Rect(0,-5000,self.lista_surface_rect.w,self.letter_size)

        self.desplazamiento = 0
        self.rodar(0)
        self.total_height = (self.lista_objetos[-1].pos.y+self.lista_objetos[-1].height) - self.lista_surface_rect.h
        self.bar_height = max(10,self.lista_surface_rect.h*(self.lista_surface_rect.h/(self.lista_objetos[-1].pos.y+self.lista_objetos[-1].height)))
        self.barra = pag.rect.Rect(self.lista_surface_rect.w - 10, 0, 10, self.bar_height)
            
        self.draw_surf()
    
    @property
    def smothscroll(self):
        return self.__smothscroll
    @smothscroll.setter
    def smothscroll(self,smothscroll):
        self.__smothscroll = smothscroll
        for x in self.lista_objetos:
            if self.smothscroll:
                x.smothmove(60, 1.5, 1, 1.5)
                # x.simple_acceleration_move(2)
            else:
                x.smothmove_bool = self.smothscroll
                
    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self,width):
        self.__width = max(width,50)
        self.size.x = self.__width
        self.resize()
        
    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self,height):
        self.__height = max(height,100)
        self.size.y = self.__height
        self.resize()

    def __getitem__(self,index):
        return self.lista_palabras[index]
    
    def __setitem__(self,index,value):
        self.lista_palabras[index] = value
        self.lista_objetos[index].text = value
    def __repr__(self):
        return '\n'.join(self.lista_palabras)
    def __str__(self) -> str:
        text = f'{'_':_>20}\n'
        text += '\n'.join(self.lista_palabras)
        text += f'\n{'-':-^20}\n'
        return text

class Multi_list(Base):
    '''
    ### More options
     - with_index
     - padding_top
     - padding_left
    
    ## Plantillas
    elif evento.type == MOUSEMOTION:
        for x in self.listas:
            if x.scroll:
                x.rodar(-evento.rel[1])
    '''
    def __init__(self, size:tuple,pos:tuple,num_lists:int=2,lista: list[list] = None, text_size: int = 20, separation: int = 0,
        background_color = 'black', selected_color = (100,100,100,100), text_color= 'white', colums_witdh= -1, header: bool =True,
        header_text: list = None, dire: str = 'topleft', fonts: list['str']|None = None, default: list[list]=None,
        smothscroll=False, **kwargs) -> None:
        
        super().__init__(pos,dire)
        self.size = Vector2(size)
        self.default = [None for _ in range(num_lists)] if not default else default
        self.lista_palabras = self.default if not lista else lista
        self.text_size = text_size
        self.separation = separation
        self.__smothscroll = smothscroll
        self.background_color = background_color
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.with_index = kwargs.get('with_index',False)
        self.text_color = text_color
        if num_lists <= 0: raise Exception('\n\nComo vas a hacer 0 listas en una multilista\nPensá bro...')
        self.num_list = num_lists
        self.colums_witdh = [((self.size.x/self.num_list)*x)/self.size.x for x in range(self.num_list)] if colums_witdh == -1 else list(colums_witdh)
        self.colums_witdh.append(1.0)
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
        self.lista_surface= pag.surface.Surface(self.rect.size)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface.fill((0,0,0))
        self.lista_surface.set_colorkey((0,0,0))
        self.lista_surface_rect.topleft = self.pos
        for x in range(num_lists):
            separar = Create_text('Hola|', self.text_size, self.fonts[-1], (0,0)).rect.h - Create_text('Hola|', self.text_size, self.fonts[0], (0,0)).rect.h

            self.listas.append(List_Box(((self.size.x*self.colums_witdh[x+1]) - (self.size.x*self.colums_witdh[x]), self.size.y),
                (self.size.x*self.colums_witdh[x],0), [self.lista_palabras[x]], self.text_size, self.separation+(separar if x != num_lists-1 else 0),
                self.selected_color, self.text_color, background_color=self.background_color, smothscroll=self.smothscroll, 
                padding_top=self.padding_top-(separar//2 if x == num_lists-1 else 0), padding_left=self.padding_left, 
                with_index=self.with_index if x == 0 and self.with_index else False,
                scroll_bar_active=False if x != num_lists-1 else True,
                header=True, text_header=self.text_header[x], header_top_left_radius=20 if x == 0 else 0, 
                header_top_right_radius=20 if x == self.num_list-1 else 0, font=self.fonts[x], header_border_color=self.border_color))
            self.lineas.append([((self.size.x*self.colums_witdh[x] -1),self.listas[0].text_header.rect.h+1), ((self.size.x*self.colums_witdh[x] -1),self.rect.h)])
        self.create_border(self.rect, 2)

    def resize(self,size):
        self.size = Vector2(size)

        self.rect = pag.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.direccion(self.rect)
        self.lista_surface= pag.surface.Surface(self.rect.size)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface.fill((0,0,0))
        self.lista_surface.set_colorkey((0,0,0))

        self.lineas.clear()
        for x in range(self.num_list):
            self.listas[x].resize(((self.size.x*self.colums_witdh[x+1]) - (self.size.x*self.colums_witdh[x]), self.size.y))
            self.listas[x].pos = (self.size.x*self.colums_witdh[x],30)
            
            self.lineas.append([((self.size.x*self.colums_witdh[x] -1),self.listas[0].text_header.rect.h+1), ((self.size.x*self.colums_witdh[x] -1),self.rect.h)])
        self.create_border(self.rect, 2)

    def draw(self,surface) -> None:
        if self.smothmove_bool:
            self.update()
        
        for x in self.listas:
            x.draw(self.lista_surface)

        for x in self.listas:
            pag.draw.rect(self.lista_surface, self.border_color, x.rect, 1)
        surface.blit(self.lista_surface,self.rect)
        
        for line in self.lineas[1:]:
            pag.draw.line(surface, self.border_color, Vector2(line[0])+self.raw_pos-(0,0)-(0,30), Vector2(line[1])+self.raw_pos-(0,1), 2)

    def rodar(self,y) -> None:
        for x in self.listas:
            x.rodar(y)
    def rodar_mouse(self,y) -> None:
        self.listas[-1].rodar_mouse(y)
        for i,x in sorted(enumerate(self.listas[:-1]),reverse=True):
            x.desplazamiento = self.listas[-1].desplazamiento
            self.rodar(0)

    def append(self,data) -> None:
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
        m = Vector2(pos) - self.pos
        
        for i,x in sorted(enumerate(self.listas),reverse=True):
            a = x.click(m)
            if a == 'scrolling' and i==len(self.listas)-1:
                self.scroll = True
                x.scroll = False
                return
            elif isinstance(a,dict):
                minilista = {'index':a['index'],'result':[l.select(a['index'], False)['text'] for l in self.listas]}
                return minilista
        for x in self.listas:
            x.select(-2000)



    def select(self, index: int = -2000) -> str:
        return [l.select(index=int(index))['text'] for l in self.listas]
        # for i,x in sorted(enumerate(self.listas),reverse=True):
        #     a = x.select(index=index)
        #     minilista = [l.select(index=int(a['index']))['text'] for l in self.listas]
        #     return minilista

    def detener_scroll(self) -> None:
        self.scroll = False
        for x in self.listas:
            x.scroll = False

    def get_list(self) -> list:
        var1 = [x.get_list() for x in self.listas]
        return list([list(x) for x in zip(*var1)])

    @property
    def smothscroll(self):
        return self.__smothscroll
    @smothscroll.setter
    def smothscroll(self,smothscroll):
        self.__smothscroll = smothscroll
        for x in self.listas:
            x.smothscroll = self.smothscroll
        

    def __getitem__(self,index: int):
        return self.listas[index]
    def __setitem__(self,index,value):
        self.listas[index] = value
    def __repr__(self) -> str:
        var = ''
        for x in self.listas:
            var += '\n'
            var += str(x)
        return var
    
