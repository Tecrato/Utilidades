from dataclasses import dataclass, field
from numpy import sin,cos,radians
from io import open
from pygame import draw
from pygame import Vector2


@dataclass
class Poligono_regular:
	__pos: list|tuple|Vector2 = field(compare=False)
	__radio: int = 20
	__lados: int =4
	__angle: int = 0
	color: list|tuple = (255,255,255,255)
	
	def __post_init__(self) -> None:
		self.x, self.y = list(self.__pos)
		if self.lados < 3: raise Exception('Para generar un poligono regular debe tener almenos 3 lados.')
		self.__generate()

	def __generate(self) -> None:
		xs = [self.x + cos(radians(360/self.__lados*a +self.__angle)) * self.__radio for a in range(self.__lados)]
		ys = [self.y - sin(radians(360/self.__lados*a +self.__angle)) * self.__radio for a in range(self.__lados)]
		self.figure = [list((x,y)) for x,y in zip(xs,ys)]

	@property
	def pos(self) -> Vector2:
		return self.__pos
	@pos.setter
	def pos(self,pos):
		self.x = pos[0]
		self.y = pos[1]
		self.__pos = Vector2(pos)
		self.__generate()
	@property
	def angle(self) -> int:
		return self.__angle
	@angle.setter
	def angle(self,angle):
		self.__angle = angle
		self.__generate()
	@property
	def radio(self) -> int:
		return self.__radio
	@radio.setter
	def radio(self,radio):
		self.__radio = radio
		self.__generate()
	@property
	def lados(self) -> int:
		return self.__lados
	@lados.setter
	def lados(self,lados):
		self.__lados = lados
		self.__generate()

	def draw(self,surface):
		draw.polygon(surface,self.color,self.figure)
	def copy(self):
		return self
	def get_edges(self) -> list:
		return self.figure


class Poligono_irregular:
	'''
	# Contiene las siguientes figuras:
	- flecha
	- estrella
	- rectangulo
	- engranaje
	- x
	- coordenadas en una lista mediante la variable type
	- nombre del archivo con un formato valido.
	'''
	def __init__(self, type, pos = (0,0), radius=20, angle= 0, **otros) -> None:
		self.x, self.y= pos
		self.__pos = Vector2(pos)
		self.__angle = angle
		self.__radio = radius
		self.type = type
		if self.type == 'engranaje':
			self.tamaño_diente =  otros.get('tamaño_diente')
			self.num_dientes = otros.get('num_dientes')
		elif self.type == 'export':
			self.archive_name = otros.get('name')
		self.color =  otros.get('color') if otros.get('color') != None else 'white'
		self.__generate()

	def __str__(self):
		return f'Poligono irregular tipo={self.type} en={self.x,self.y} angle={self.__angle}'

	def __generate(self) -> None:
		if self.type == 'flecha':
			self.figure = [
				[self.x + cos(radians(self.__angle)) * self.radio,self.y - sin(radians(self.__angle)) * self.radio],
				[self.x + cos(radians(self.__angle+90)) * self.radio*.8,self.y - sin(radians(self.__angle+90)) * self.radio*.8],
				[self.x + cos(radians(self.__angle+90)) * self.radio*.25,self.y - sin(radians(self.__angle+90)) * self.radio*.25],
				[self.x + cos(radians(self.__angle+165)) * self.radio,self.y - sin(radians(self.__angle+165)) * self.radio],
				[self.x + cos(radians(self.__angle+195)) * self.radio,self.y - sin(radians(self.__angle+195)) * self.radio],
				[self.x + cos(radians(self.__angle-90)) * self.radio*.25,self.y - sin(radians(self.__angle-90)) * self.radio*.25],
				[self.x + cos(radians(self.__angle-90)) * self.radio*.8,self.y - sin(radians(self.__angle-90)) * self.radio*.8],
			]
		elif self.type == 'estrella':
			self.figure = [(self.x + cos(radians(360/5* (.5*x) + self.__angle))*self.radio/(2 if x%2==0 else 1),self.y - sin(radians(360/5* (.5*x) + self.__angle)) * self.radio/(2 if x%2==0 else 1)) for x in range(10)]
		elif self.type == 'rectangulo':
			self.figure = [
				[self.x + cos(radians(-10 + self.__angle))*self.radio,self.y - sin(radians(-10 + self.__angle)) * self.radio],
				[self.x + cos(radians(10 + self.__angle))*self.radio,self.y - sin(radians(10 + self.__angle)) * self.radio],
				[self.x + cos(radians(170 + self.__angle))*self.radio,self.y - sin(radians(170 + self.__angle)) * self.radio],
				[self.x + cos(radians(190 + self.__angle))*self.radio,self.y - sin(radians(190 + self.__angle)) * self.radio],
			]
		elif self.type == 'engranaje':
			self.figure = [Poligono_regular((self.x + cos(radians(360/self.num_dientes*a +self.__angle+45)) * self.radio,self.y - sin(radians(360/self.num_dientes*a +self.__angle+45)) * self.radio), self.tamaño_diente,4,360/self.num_dientes*a +self.__angle) for a in range(self.num_dientes)]
		elif self.type == 'x':
			self.figure = [
				[self.x + cos(radians(350  + self.__angle))*self.radio,self.y - sin(radians(350  + self.__angle)) * self.radio],
				[self.x + cos(radians(10  + self.__angle))*self.radio,self.y - sin(radians(10  + self.__angle)) * self.radio],
				[self.x + cos(radians(45  + self.__angle))*(self.radio/4),self.y - sin(radians(45  + self.__angle)) * (self.radio/4)],
				[self.x + cos(radians(80  + self.__angle))*self.radio,self.y - sin(radians(80  + self.__angle)) * self.radio],
				[self.x + cos(radians(100  + self.__angle))*self.radio,self.y - sin(radians(100  + self.__angle)) * self.radio],
				[self.x + cos(radians(135  + self.__angle))*(self.radio/4),self.y - sin(radians(135  + self.__angle)) * (self.radio/4)],
				[self.x + cos(radians(170  + self.__angle))*self.radio,self.y - sin(radians(170  + self.__angle)) * self.radio],
				[self.x + cos(radians(190  + self.__angle))*self.radio,self.y - sin(radians(190  + self.__angle)) * self.radio],
				[self.x + cos(radians(225  + self.__angle))*(self.radio/4),self.y - sin(radians(225  + self.__angle)) * (self.radio/4)],
				[self.x + cos(radians(260  + self.__angle))*self.radio,self.y - sin(radians(260  + self.__angle)) * self.radio],
				[self.x + cos(radians(280  + self.__angle))*self.radio,self.y - sin(radians(280  + self.__angle)) * self.radio],
				[self.x + cos(radians(315  + self.__angle))*(self.radio/4),self.y - sin(radians(315  + self.__angle)) * (self.radio/4)],
			]
		elif self.type == 'export':
			string = [{'angle':float(a), 'radio':float(s)} for a,s in [x.split(',') for x in open(f'{self.archive_name}.txt','r').read().split('|')]]
			self.figure = [(self.x + cos(radians(l['angle'] + self.__angle))*self.radio,self.y - sin(radians(l['angle'] + self.__angle)) * self.radio) for l in string]
		else:
			self.figure = self.generate_irregluar_polygon(self.type)

	def generate_irregluar_polygon(self,l):
		nose = []
		xs = [self.x + cos(radians(a['angle'])) * a['radio'] for a in l]
		ys = [self.y - sin(radians(a['angle'])) * a['radio'] for a in l]
		for x,y in zip(xs,ys):
			nose.append(list((x,y)))
		return nose

	@property
	def pos(self) -> Vector2:
		return self.__pos
	@pos.setter
	def pos(self,pos):
		self.x = pos[0]
		self.y = pos[1]
		self.__pos = Vector2(pos)
		self.__generate()
	@property
	def angle(self) -> int:
		return self.__angle
	@angle.setter
	def angle(self,angle):
		self.__angle = angle
		self.__generate()
	@property
	def radio(self) -> int:
		return self.__radio
	@radio.setter
	def radio(self,radio):
		self.__radio = radio
		self.__generate()
	@property
	def lados(self) -> int:
		return self.__lados
	@lados.setter
	def lados(self,lados):
		self.__lados = lados
		self.__generate()

	def draw(self,surface) -> None:
		if self.type in ['flecha','estrella','rectangulo','diamante']:
			draw.polygon(surface,self.color, self.figure)
		elif self.type == 'engranaje':
			draw.circle(surface, self.color, (self.x,self.y),self.radio)
			for x in self.figure:
				draw.polygon(surface,self.color,x.figure)
		else:
			draw.polygon(surface,self.color, self.figure)

	def copy(self):
		return self
	def get_edges(self):
		return self.figure