from .base import Base
from math import cos, sin, radians
from array import array

class Poligono_regular(Base):
	def __init__(self, pos = array('f',[0,0]), lados = 4, radio = 10, angle = 0) -> None:
		super().__init__(pos,radio,angle)
		self.__lados = lados
		self.__angle = angle
		assert self.lados > 3
		self.generate()

	def generate(self) -> None:
		xs = [self.pos[0] + cos(radians(360/self.__lados*a +self.angle)) * self.radio for a in range(self.__lados)]
		ys = [self.pos[1] - sin(radians(360/self.__lados*a +self.angle)) * self.radio for a in range(self.__lados)]
		self.figure = [(int(x),int(y)) for x,y in zip(xs,ys)]

	@property
	def lados(self) -> int:
		return self.__lados
	@lados.setter
	def lados(self,lados):
		self.__lados = lados
		self.generate()

	def __len__(self):
		return len(self.figure)

	def __getitem__(self, index):
		return self.figure[index]

	def __setitem__(self, index, value: list[int,int]):
		self.figure[index] = value
