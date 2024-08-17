import pygame as pag
from Utilidades.obj_Base import Base
from PIL import Image as img
from io import BytesIO

class Image(Base):
    def __init__(self,image,pos,direccion: str = 'center', size = None,color_key=(254,1,1), dir=[1,0],vel=1):
        super().__init__(pos,direccion)
        self.path: str = image
        self.__size = tuple(size)
        self.color_key = color_key

        

        self.cache = {}
        self.generate_img()

        self.simple_acceleration_move(vel,dir,'forward')

        self.direccion(self.rect)


    def generate_img(self):
        if str(self.__size)+str(self.color_key) in self.cache:
            self.surf = self.cache[str(self.__size) + str(self.color_key)]
            self.rect = self.surf.get_rect()
            return

        if self.__size:
            im = img.open(self.path).resize((int(self.__size[0]), int(self.__size[1])))
            img_bytes = BytesIO()
            im.save(img_bytes,'PNG')
            img_bytes.seek(0)
            self.surf = pag.Surface((im.size))
            self.image = pag.image.load(img_bytes)
        else:
            self.image = pag.image.load(self.path).convert()
            self.surf = pag.Surface(self.image.get_size())
        self.surf.fill(self.color_key)
        self.surf.set_colorkey(self.color_key)
        self.surf.blit(self.image,(0,0))
        self.rect = self.image.get_rect()

        self.cache[str(self.__size) + str(self.color_key)] = self.surf



    @property
    def size(self):
        return self.__size
    @size.setter
    def size(self,size):
        self.__size = pag.Vector2(size)
        self.generate_img()


    def draw(self,surface: pag.Surface):
        surface.blit(self.surf,self.rect)
