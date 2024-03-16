from dataclasses import dataclass, field
from numpy import sin,cos,radians
from io import open
from pygame import draw
from pygame import Vector2


@dataclass
class Poligono_regular:
	pos: list|tuple = field(compare=False)
	radio: int = 20
	lados: int =4
	angle: int = 0
	color: list|tuple = (255,255,255,255)
	
	def __post_init__(self) -> None:
		self.x, self.y = list(self.pos)
		if self.lados < 3: raise Exception('Para generar un poligono regular debe tener almenos 3 lados.')
		self.__generate()

	def __generate(self) -> None:
		nose = []
		xs = [self.x + cos(radians(360/self.lados*a +self.angle)) * self.radio for a in range(self.lados+1)]
		ys = [self.y - sin(radians(360/self.lados*a +self.angle)) * self.radio for a in range(self.lados+1)]
		for x,y in zip(xs,ys):
			nose.append(list((x,y)))
		self.figure = nose

	def move(self,x=None,y=None,angle=None,radio=None) -> None:
		self.pos[0]=x if x != None else self.pos[0]
		self.pos[1]=y if y != None else self.pos[1]
		self.angle=angle if angle != None else self.angle
		self.radio=radio if radio != None else self.radio
		if x or y and not (angle or radio):
			for x in self.figure:
				x[0] += (self.pos[0] - x[0])
				x[1] += (self.pos[1] - x[1])
		elif angle or radio:
			self.__generate()


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
		self.angle = angle
		self.radio = radius
		self.type = type
		if self.type == 'engranaje':
			self.tamaño_diente =  otros.get('tamaño_diente')
			self.num_dientes = otros.get('num_dientes')
		elif self.type == 'export':
			self.archive_name = otros.get('name')
		self.color =  otros.get('color') if otros.get('color') != None else 'white'
		self.__generate()

	def __str__(self):
		return f'Poligono irregular tipo={self.type} en={self.x,self.y} angle={self.angle}'

	def __generate(self) -> None:
		if self.type == 'flecha':
			self.figure = [
				[self.x + cos(radians(self.angle)) * self.radio,self.y - sin(radians(self.angle)) * self.radio],
				[self.x + cos(radians(self.angle+90)) * self.radio*.8,self.y - sin(radians(self.angle+90)) * self.radio*.8],
				[self.x + cos(radians(self.angle+90)) * self.radio*.25,self.y - sin(radians(self.angle+90)) * self.radio*.25],
				[self.x + cos(radians(self.angle+165)) * self.radio,self.y - sin(radians(self.angle+165)) * self.radio],
				[self.x + cos(radians(self.angle+195)) * self.radio,self.y - sin(radians(self.angle+195)) * self.radio],
				[self.x + cos(radians(self.angle-90)) * self.radio*.25,self.y - sin(radians(self.angle-90)) * self.radio*.25],
				[self.x + cos(radians(self.angle-90)) * self.radio*.8,self.y - sin(radians(self.angle-90)) * self.radio*.8],
				[self.x + cos(radians(self.angle)) * self.radio,self.y - sin(radians(self.angle)) * self.radio],
			]
		elif self.type == 'estrella':
			self.figure = [(self.x + cos(radians(360/5* (.5*x) + self.angle))*self.radio/(2 if x%2==0 else 1),self.y - sin(radians(360/5* (.5*x) + self.angle)) * self.radio/(2 if x%2==0 else 1)) for x in range(11)]
		elif self.type == 'rectangulo':
			self.figure = [
				[self.x + cos(radians(-10 + self.angle))*self.radio,self.y - sin(radians(-10 + self.angle)) * self.radio],
				[self.x + cos(radians(10 + self.angle))*self.radio,self.y - sin(radians(10 + self.angle)) * self.radio],
				[self.x + cos(radians(170 + self.angle))*self.radio,self.y - sin(radians(170 + self.angle)) * self.radio],
				[self.x + cos(radians(190 + self.angle))*self.radio,self.y - sin(radians(190 + self.angle)) * self.radio],
				[self.x + cos(radians(-10 + self.angle))*self.radio,self.y - sin(radians(-10 + self.angle)) * self.radio],
			]
		elif self.type == 'engranaje':
			self.figure = [Poligono_regular((self.x + cos(radians(360/self.num_dientes*a +self.angle+45)) * self.radio,self.y - sin(radians(360/self.num_dientes*a +self.angle+45)) * self.radio), self.tamaño_diente,4,360/self.num_dientes*a +self.angle) for a in range(self.num_dientes)]
		elif self.type == 'x':
			self.figure = [
				[self.x + cos(radians(350  + self.angle))*self.radio,self.y - sin(radians(350  + self.angle)) * self.radio],
				[self.x + cos(radians(10  + self.angle))*self.radio,self.y - sin(radians(10  + self.angle)) * self.radio],
				[self.x + cos(radians(45  + self.angle))*(self.radio/4),self.y - sin(radians(45  + self.angle)) * (self.radio/4)],
				[self.x + cos(radians(80  + self.angle))*self.radio,self.y - sin(radians(80  + self.angle)) * self.radio],
				[self.x + cos(radians(100  + self.angle))*self.radio,self.y - sin(radians(100  + self.angle)) * self.radio],
				[self.x + cos(radians(135  + self.angle))*(self.radio/4),self.y - sin(radians(135  + self.angle)) * (self.radio/4)],
				[self.x + cos(radians(170  + self.angle))*self.radio,self.y - sin(radians(170  + self.angle)) * self.radio],
				[self.x + cos(radians(190  + self.angle))*self.radio,self.y - sin(radians(190  + self.angle)) * self.radio],
				[self.x + cos(radians(225  + self.angle))*(self.radio/4),self.y - sin(radians(225  + self.angle)) * (self.radio/4)],
				[self.x + cos(radians(260  + self.angle))*self.radio,self.y - sin(radians(260  + self.angle)) * self.radio],
				[self.x + cos(radians(280  + self.angle))*self.radio,self.y - sin(radians(280  + self.angle)) * self.radio],
				[self.x + cos(radians(315  + self.angle))*(self.radio/4),self.y - sin(radians(315  + self.angle)) * (self.radio/4)],
				[self.x + cos(radians(350  + self.angle))*self.radio,self.y - sin(radians(350  + self.angle)) * self.radio],
			]
		elif self.type == 'export':
			string = [{'angle':float(a), 'radio':float(s)} for a,s in [x.split(',') for x in open(f'{self.archive_name}.txt','r').read().split('|')]]
			self.figure = [(self.x + cos(radians(l['angle'] + self.angle))*self.radio,self.y - sin(radians(l['angle'] + self.angle)) * self.radio) for l in string]
		else:
			self.figure = self.generate_irregluar_polygon(self.type)

	def generate_irregluar_polygon(self,l):
		nose = []
		xs = [self.x + cos(radians(a['angle'])) * a['radio'] for a in l]
		ys = [self.y - sin(radians(a['angle'])) * a['radio'] for a in l]
		for x,y in zip(xs,ys):
			nose.append(list((x,y)))
		return nose

	def move(self,x=None,y=None,angle=None,radio=None) -> None:
		self.pos[0]=x if x != None else self.pos[0]
		self.pos[1]=y if y != None else self.pos[1]
		self.angle=angle if angle != None else self.angle
		self.radio=radio if radio != None else self.radio
		if x or y and not (angle or radio):
			for x in self.figure:
				x[0] += (self.pos[0] - x[0])
				x[1] += (self.pos[1] - x[1])
		elif angle or radio:
			self.__generate()
	def move_sum(self,x:int=None,y:int=None,angle:int=None,radio:int=None,dt:float=1.0) -> None:
		self.x=self.x+(x*dt) if x != None else self.x
		self.y=self.y+(y*dt) if y != None else self.y
		self.angle=self.angle + angle*dt if angle != None else self.angle
		self.radio=self.radio+radio*dt if radio != None else self.radio
		if x or y and not (angle or radio):
			for x in self.figure:
				x[0] += (self.pos[0] - x[0])
				x[1] += (self.pos[1] - x[1])
		elif angle or radio:
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