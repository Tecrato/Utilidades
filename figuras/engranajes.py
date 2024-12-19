from .base import Base
from math import cos, sin, radians
from .poligono_regular import Poligono_regular

class Engranaje(Base):
	def __init__(self,pos, dientes, size_diente, radio,angle=0) -> None:
		super().__init__(pos,radio,angle)
		self.n_dientes = dientes
		self.size_diente = size_diente
		self.dientes = []

	def generate(self) -> None:
		self.dientes = [Poligono_regular((self.pos[0] + cos(radians(360/self.n_dientes*a +self.angle+45)) * self.radio,self.pos[1] - sin(radians(360/self.n_dientes*a +self.angle+45)) * self.radio),4, self.size_diente,360/self.n_dientes*a +self.angle) for a in range(self.n_dientes)]
		
	# def draw(self,surface) -> Rect:
	# 	for x in self.dientes:
	# 		draw.polygon(surface,self.color,x.figure)
	# 	draw.circle(surface, self.color, self.pos,self.radio)
		
	# 	s = (self.radio + self.size_diente)
	# 	return Rect(0,0,s*2,s*2).move(self.pos[0]-s,self.pos[1]-s)
