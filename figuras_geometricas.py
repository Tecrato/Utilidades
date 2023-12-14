import pygame as pag
from numpy import sin,cos,radians
from io import open


class Poligono_regular:
	def __init__(self, pos:tuple=(0,0), angle= 0, radius = 20, lados=4):
		self.pos = pos
		self.x, self.y= self.pos
		self.radio = radius
		self.angle = angle
		self.lados = lados
		if lados < 3: raise Exception('Para generar un poligono regular debe tener almenos 3 lados.')
		self.__generate()

	def __generate(self):
		nose = []
		xs = [self.x + cos(radians(360/self.lados*a +self.angle)) * self.radio for a in range(self.lados)]
		ys = [self.y - sin(radians(360/self.lados*a +self.angle)) * self.radio for a in range(self.lados)]
		for x,y in zip(xs,ys):
			nose.append(list((x,y)))
		self.figure = nose

	def move(self,x=None,y=None,angle=None,radius=None):
		self.x=x if x != None else self.x
		self.y=y if y != None else self.y
		self.angle=angle if angle != None else self.angle
		self.radio=radius if radius != None else self.radio
		self.__generate()

	def draw(self, surface):
		pag.draw.polygon(surface, 'white', self.figure)

	def copy(self):
		return self
	def get_edges(self):
		return self.figure


class Poligono_irregular:
	def __init__(self, type, pos = (0,0), angle= 0, radius=20, **otros) -> None:
		self.x, self.y= pos
		self.angle = angle
		self.radio = radius
		self.type = type
		self.rectangle_n =  otros.get('rect_n')
		if self.type == 'engranaje':
			self.diente =  otros.get('diente')
			self.n = otros.get('n')
		elif self.type == 'export':
			self.archive_name = otros.get('name')
			self.n = otros.get('n')
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
			]
		elif self.type == 'estrella':
			self.figure = [(self.x + cos(radians(360/5* (.5*x) + self.angle))*self.radio/(2 if x%2==0 else 1),self.y - sin(radians(360/5* (.5*x) + self.angle)) * self.radio/(2 if x%2==0 else 1)) for x in range(11)]
		elif self.type == 'rectangulo':
			self.figure = [
				[self.x + cos(radians(-10 + self.angle))*self.radio,self.y - sin(radians(-10 + self.angle)) * self.radio],
				[self.x + cos(radians(10 + self.angle))*self.radio,self.y - sin(radians(10 + self.angle)) * self.radio],
				[self.x + cos(radians(170 + self.angle))*self.radio,self.y - sin(radians(170 + self.angle)) * self.radio],
				[self.x + cos(radians(190 + self.angle))*self.radio,self.y - sin(radians(190 + self.angle)) * self.radio],
			]
		elif self.type == 'engranaje':
			self.figure = [Poligono_regular((self.x + cos(radians(360/self.n*a +self.angle+45)) * self.radio,self.y - sin(radians(360/self.n*a +self.angle+45)) * self.radio),360/self.n*a +self.angle, self.diente) for a in range(self.n)]
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
		self.x=x if x != None else self.x
		self.y=y if y != None else self.y
		self.angle=angle if angle != None else self.angle
		self.radio=radio if radio != None else self.radio
		self.__generate()

	def draw(self,surface):
		if self.type in ['flecha','estrella','rectangulo','diamante']:
			pag.draw.polygon(surface,self.color, self.figure)
		elif self.type == 'engranaje':
			pag.draw.circle(surface, self.color, (self.x,self.y),self.radio)
			for x in self.figure:
				pag.draw.polygon(surface,self.color,x.figure)
		else:
			pag.draw.polygon(surface,self.color, self.figure)

	def copy(self):
		return self
	def get_edges(self):
		return self.figure