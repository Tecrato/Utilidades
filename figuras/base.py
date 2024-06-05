from typing import Self
from numpy import sin,cos,radians
from io import open
from pygame import draw
from pygame import Vector2
from pathlib import Path

class Base:
	def __init__(self,pos,radio,angle,color) -> None:
		self.__pos = Vector2(pos)
		self.__angle = angle
		self.__radio = radio
		self.__color = color

	def draw(self,surface):
		draw.polygon(surface,self.color,self.figure)
	


	@property
	def pos(self) -> Vector2:
		return self.__pos
	@pos.setter
	def pos(self,pos):
		self.x = pos[0]
		self.y = pos[1]
		self.__pos = Vector2(pos)
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

