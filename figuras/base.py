from typing import Self

from array import array

class Base:
	def __init__(self,pos: list[int|float]|tuple[int|float],angle: float,radio: int,color: tuple[int,int,int]):
		self.__pos = array('f',pos)
		self.x = self.__pos.x
		self.y = self.__pos.y
		self.__angle = angle
		self.__radio = radio
		self.__color = color
		self.max_radio = 0
		self.figure: list[dict] = []

	@property
	def pos(self) -> array:
		return self.__pos
	@pos.setter
	def pos(self,pos):
		self.x = pos[0]
		self.y = pos[1]
		self.__pos = array('f',pos)
		self.generate()
	@property
	def angle(self) -> float:
		return float(self.__angle)
	@angle.setter
	def angle(self,angle):
		self.__angle = float(angle)
		self.generate()
	@property
	def radio(self) -> int:
		return self.__radio
	@radio.setter
	def radio(self,radio):
		self.__radio = int(radio)
		self.generate()
	@property
	def color(self):
		return self.__color
	@color.setter
	def color(self,color):
		self.__color = color

	def copy(self) -> Self:
		return self
	@property
	def edges(self) -> list:
		return self.figure

