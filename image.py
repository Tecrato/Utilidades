import pygame as pag
from Utilidades.obj_Base import Base
from PIL import Image as img
from io import BytesIO

class Image(Base):
    def __init__(self,image,pos,direccion: str = 'center', size = None,color_key=(254,1,1), dir=[1,0],vel=1):
        super().__init__(pos,direccion)
        self.path: str = image
        if size:
            im = img.open(self.path).resize(size)
            img_bytes = BytesIO()
            im.save(img_bytes,'PNG')
            img_bytes.seek(0)
            self.surf = pag.Surface((im.size))
            self.image = pag.image.load(img_bytes)
        else:
            self.image = pag.image.load(self.path).convert()
            self.surf = pag.Surface(self.image.get_size())
        self.surf.fill(color_key)
        self.surf.set_colorkey(color_key)
        self.surf.blit(self.image,(0,0))
        self.rect = self.image.get_rect()

        self.vel = pag.Vector2(dir)*vel

        self.direccion(self.rect)

    def draw(self,surface: pag.Surface):
        surface.blit(self.surf,self.rect)
