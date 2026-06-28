from typing import Tuple
from math import cos, sin, radians
from .base import BasePolygon

class Engranaje(BasePolygon):
	def __init__(
			self, pos: Tuple[float, float], 
			dientes: int, 
			size_diente: float, 
			radio: float, 
			angle: float = 0, 
			color: Tuple[int, int, int] = (255, 255, 255),
		):
		
		super().__init__(pos, radio, angle, cell_size)
		self.__n_dientes = dientes
		self.__size_diente = size_diente
		self.color = color
		self.__generate()

	def __generate(self):
		"""Generación precisa de dientes cuadrados radiales"""
		vertices = []
		paso_angular = 360 / self.n_dientes
		radio_total = self.radio + self.__size_diente
		
		for i in range(self.n_dientes):
			angulo_central = radians(paso_angular * i + self._angle)
			
			# Base inicio
			vertices.append(
				(
					self.pos[0] + cos(angulo_central - radians(paso_angular/4)) * self.radio,
					self.pos[1] - sin(angulo_central - radians(paso_angular/4)) * self.radio
				)
			)
			# Punta inicio
			vertices.append(
				(
					self.pos[0] + cos(angulo_central - radians(paso_angular/8)) * radio_total,
					self.pos[1] - sin(angulo_central - radians(paso_angular/8)) * radio_total
				)
			)

			# Base fin
			vertices.append(
				(
					self.pos[0] + cos(angulo_central + radians(paso_angular/8)) * radio_total,
					self.pos[1] - sin(angulo_central + radians(paso_angular/8)) * radio_total
				)
			)
			# Punta fin
			vertices.append(
				(
					self.pos[0] + cos(angulo_central + radians(paso_angular/4)) * self.radio,
					self.pos[1] - sin(angulo_central + radians(paso_angular/4)) * self.radio
				)
			)
			
		# Suavizar transiciones entre dientes
		self._figure = vertices
		self.update_rect()

	# Setters actualizados para regeneración automática
	@property
	def n_dientes(self) -> int:
		return self.__n_dientes
	@n_dientes.setter
	def n_dientes(self, value: int):
		if value != self.__n_dientes and value > 3:
			self.__n_dientes = value
			self.__generate()

	@property
	def size_diente(self) -> float:
		return self.__size_diente
	@size_diente.setter
	def size_diente(self, value: float):
		if value != self.__size_diente:
			self.__size_diente = value
			self.__generate()