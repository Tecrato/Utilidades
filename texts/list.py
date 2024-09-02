import pygame as pag
from pygame.math import Vector2
from ..obj_Base import Base
from .text import Text
from ..Animaciones import Second_Order_Dinamics



class List(Base):
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
        background_color = 'black', font=None, smothscroll=False, dire='topleft',border_width=2,border_radius=20, **kwargs) -> None:

        super().__init__(pos,dire)
        self.__size = Vector2(size)
        self.__width = size[0]
        self.__height = size[1]
        self.text_size = text_size
        self.__smothscroll = smothscroll
        self.background_color = background_color
        self.selected_color = selected_color
        self.padding_top = kwargs.get('padding_top',10)
        self.padding_left = kwargs.get('padding_left',20)
        self.border_width = border_width
        self.border_radius = border_radius
        self.text_color = text_color
        self.header = header
        self.text_header = text_header
        self.font = font
        self.separacion = separation

        self.header_top_right_radius = kwargs.get('header_top_right_radius',20)
        self.header_top_left_radius = kwargs.get('header_top_left_radius',20)
        self.header_border_color = kwargs.get('header_border_color',20)
        self.scroll_bar_active = kwargs.get('scroll_bar_active',True)

        self.letter_size = Text('ssss|', self.text_size, self.font, (0,0),padding= self.separacion).rect.height

        if not lista:
            self.first_insert = True
            self.lista_palabras = ['None']
        else:
            self.lista_palabras = lista
            self.first_insert = False
        self.lista_objetos: list[Text] = []

        self.barra = pag.rect.Rect(0, 0, 15, 50)
        
        self.desplazamiento = 0
        self.total_content_height = 0
        self.smothscroll_movent = Second_Order_Dinamics(60, 1.5, 1, 1.5,0)
        self.desplazamiento_smoth = 0
        
        self.scroll = False

        

        self.__generate()
    
    def __generate(self):

        if self.header:
            self.text_header: Text = Text(self.text_header, 23, None, self.pos, 'bottomleft', 'black', True, 'darkgrey',
            padding=(5,15),border_width=1, border_top_left_radius=self.header_top_left_radius,
            border_top_right_radius=self.header_top_right_radius, border_color=self.header_border_color, width=self.size[0])
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1]+self.text_header.rect.h, self.size[0], self.size[1]-self.text_header.rect.h)
            self.text_header.bottomleft = self.rect.topleft
        else:
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        self.lista_surface= pag.surface.Surface(self.rect.size)
        self.lista_surface_rect = self.lista_surface.get_rect()
        self.lista_surface_rect.topleft = self.pos
        self.lista_surface.fill((254,1,1))
        self.lista_surface.set_colorkey((254,1,1))



        #cuadro de seleccion
        self.select_box = pag.rect.Rect(0,-5000,self.lista_surface_rect.w,self.letter_size)
        self.selected_nums: list[int] = []

        self.actualizar_lista()
        self.mover_textos()

        #La barra que sube y baja
        self.bar_height = max(10,self.lista_surface_rect.h*(self.lista_surface_rect.h/self.lista_objetos[-1].rect.bottom))
        self.barra = pag.rect.Rect(self.lista_surface_rect.w - 13, 0, 13, self.bar_height)
        

        self.draw_surf()
        self.create_border(self.rect.union(self.text_header.rect), self.border_width)


    def resize(self, size):
        self.__width = max(size[0],30)
        self.__height = max(size[1],20)
        self.__size = Vector2(self.__width,self.__height)
        if self.header:
            self.rect = pag.rect.Rect(self.pos[0], self.pos[1]+self.text_header.height, self.size[0], self.size[1]-self.text_header.height)
            self.text_header.width = self.size[0]
            self.text_header.bottomleft = self.rect.topleft
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

        self.reset_height()
        self.barra.right = self.lista_surface_rect.w

        self.rodar(0)
        if self.scroll_bar_active and self.total_content_height>0:
            self.barra.top = -(self.lista_surface_rect.h-self.barra.h) * (self.desplazamiento / self.total_content_height)
        else:
            self.barra.top = 0

        self.select(self.selected_nums[0] if self.selected_nums else -2000,more=True)
        self.create_border(self.rect.union(self.text_header.rect), self.border_width)
        self.draw_surf()
    
    def draw_surf(self):
        self.lista_surface.fill(self.background_color)

        if len(self.selected_nums) > 0:
            for num in self.selected_nums:
                self.select_box.centery = self.lista_objetos[num].centery
                pag.draw.rect(self.lista_surface, self.selected_color, self.select_box)

        self.lista_surface.blits([(te.text_surf,te.rect_text) for te in self.lista_objetos])
            
        if self.scroll_bar_active and self.total_content_height + self.lista_surface_rect.h > self.rect.h:
            pag.draw.rect(self.lista_surface, 'white', self.barra,border_radius=5)


    def mover_textos(self):
        for num ,text in enumerate(self.lista_objetos):
            text.update((self.padding_left,(self.letter_size*num) + self.padding_top + (self.desplazamiento_smoth if self.smothscroll else self.desplazamiento)))

    def update(self,dt=1):

        if self.smothscroll:
            self.desplazamiento_smoth = self.smothscroll_movent.update(self.desplazamiento,dt=dt).x
            self.mover_textos()
        super().update(dt=dt)
        self.text_header.bottomleft = self.rect.topleft
        self.rect_border.bottom = self.rect.bottom

    def draw(self,surface: pag.Surface) -> None:

        if self.smothscroll and self.lista_objetos and abs(sum(self.smothscroll_movent.yd.xy)) > 0.1:
            self.draw_surf()

        if self.header:
            self.text_header.draw(surface)

        surface.blit(self.lista_surface,self.rect)
        pag.draw.rect(surface, 'black', self.rect_border, self.border_width, border_radius=self.border_radius, border_bottom_left_radius=0, border_bottom_right_radius=0)
        
        return self.rect

    def reset_height(self):
        if self.lista_objetos:
            # self.total_content_height = self.lista_objetos[-1].rect.bottom - self.lista_surface_rect.h
            self.total_content_height = (self.letter_size*len(self.lista_palabras)) + self.padding_top - self.rect.height + 10
            # self.total_content_height = (self.lista_objetos[-1].height*len(self.lista_palabras)) + self.padding_top - self.rect.height*2 + 10
        else:
            self.total_content_height = 0
        self.bar_height = max(10,self.lista_surface_rect.h*(self.lista_surface_rect.h/(self.total_content_height + self.rect.height)))
        self.barra.h = self.bar_height

    def actualizar_lista(self) -> None:
        self.lista_objetos.clear()
        for num ,text in enumerate(self.lista_palabras):
            self.lista_objetos.append(Text(text, self.text_size, self.font, (self.padding_left,(self.letter_size*num) + self.padding_top), 'topleft', self.text_color, padding=20))

        self.reset_height()
        self.rodar(0)
        self.draw_surf()

    def append(self,texto:str) -> None:
        if self.first_insert:
            self.lista_palabras.clear()
            self.lista_objetos.clear()
        self.lista_palabras.append(str(texto))
        self.lista_objetos.append(Text(texto, self.text_size, self.font, (self.padding_left,(self.letter_size*(len(self.lista_palabras)-1)) + self.padding_top), 'topleft', self.text_color, padding=20))

        self.reset_height()
        self.first_insert = False
        self.rodar(0)
        self.draw_surf()

    def change_list(self, lista: list) -> None:
        if not isinstance(lista, list) or len(lista) == 0:
            return
        self.lista_palabras: list[str] = lista
        self.first_insert = False
        self.selected_nums.clear()
        self.actualizar_lista()

    def clear(self) -> None:
        self.selected_nums.clear()
        self.lista_objetos.clear()
        self.lista_palabras = ['None']
        self.first_insert = True
        self.actualizar_lista()
        if not self.smothscroll:
            self.draw_surf()

    def click(self,pos, shift=False, button=1):
        if not self.rect.collidepoint(pos):
            self.select(-2000)
            return False
        m = Vector2(pos)
        m -= self.rect.topleft
        m += (0,5)
        if self.scroll_bar_active and self.barra.collidepoint(m):
            self.scroll = True
            return 'scrolling'
        for index, te in enumerate(self.lista_objetos):
            if te.top < m.y < te.bottom:
                self.select(index, False, shift, button)
                return {'index': index,'text': te.text}
        self.select(-2000)

    def select(self, index: int = -2000, diff = True, more = False,button=1) -> dict|bool:
        if index != -2000:
            if (not more and index not in self.selected_nums) or (button == 1 and not more):
                self.selected_nums.clear()
            if index not in self.selected_nums:
                self.selected_nums.append(index)
            if diff:
                self.desplazamiento = (-self.letter_size*(index+1) + self.padding_top) + self.lista_surface_rect.h/2
            self.rodar(0)
            self.draw_surf()
            return {'text': self.lista_objetos[index].raw_text, 'index': index}

        self.selected_nums.clear()
        self.rodar(0)
        self.draw_surf()
        return False

    def rodar(self,y) -> None:
        if self.total_content_height + self.lista_surface_rect.h < self.rect.h:
            return

        self.desplazamiento += y
        self.desplazamiento = min(0,self.desplazamiento)
        self.desplazamiento = max(-self.total_content_height,self.desplazamiento)
                
        if self.scroll_bar_active and self.total_content_height>0:
            self.barra.top = -(self.lista_surface_rect.h-self.barra.h) * (self.desplazamiento / self.total_content_height)
        else:
            self.barra.top = 0

        self.mover_textos()

        if not self.smothscroll:
            self.draw_surf()


    def rodar_mouse(self,rel):
        self.barra.centery += rel
        if self.barra.top <= 0:
            self.barra.top = 0
            self.desplazamiento = 0
            self.rodar(0)
            return
        self.desplazamiento = -(self.total_content_height / ((self.lista_surface_rect.h - self.barra.h) / self.barra.top))
        self.rodar(0)

    def get_list(self) -> list[str]:
        return self.lista_palabras

    def pop(self,index=-1):
        if len(self.lista_palabras) < 1:
            return
        self.lista_objetos.pop(index)
        self.lista_palabras.pop(index)
        if len(self.lista_palabras) < 1:
            self.lista_palabras = ['None']
        self.selected_nums = [index-1] if index != -1 else []

        self.reset_height()

        self.rodar(0)
        self.select(index-1)
        self.draw_surf()

    def get_selects(self) -> list[str]:
        # print(self.lista_palabras,len(self.lista_palabras),len(self.lista_objetos),self.lista_objetos)
        return [(x,self.lista_palabras[x]) for x in self.selected_nums]

    @property
    def smothscroll(self):
        return self.__smothscroll
    @smothscroll.setter
    def smothscroll(self,smothscroll):
        self.__smothscroll = bool(smothscroll)
                
    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self,size):
        self.resize(size)
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

    def __len__(self):
        return len(self.lista_palabras)

    def __getitem__(self,index):
        return self.lista_palabras[index]
    
    def __setitem__(self,index,value):
        self.lista_palabras[index] = value
        self.lista_objetos[index].text = value
        self.draw_surf()
    def __repr__(self):
        return '\n'.join(self.lista_palabras)
    def __str__(self) -> str:
        text = f'{'_':_>20}\n'
        text += '\n'.join(self.lista_palabras)
        text += f'\n{'-':-^20}\n'
        return text
