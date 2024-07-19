from pathlib import Path
from .base import Base
from math import cos, sin, radians

class Poligono_irregular(Base):
	'''
	# Contiene las siguientes figuras pre-establecidas:
	- "flecha"
	- "estrella"
	- "rectangulo"
	- "engranaje"
	- "x"
	## O tambien puede personalizar su figura:
	- coordenadas en una lista mediante la variable type
	- nombre del archivo con un formato valido.
	'''
	def __init__(self, type, pos = (0,0), radio=20, angle=0,color='white') -> None:
		super().__init__(pos,radio,angle,color)
		self.type = type
		self.generate()

	def generate(self) -> None:
		if self.type in ['flecha','x','rectangulo','estrella']:
			self.import_file(f'./{self.type}.txt')
		elif isinstance(self.type,(list,tuple)):
			self.figure = self.type
		else:
			self.figure = self.generate_irregluar_polygon(self.type)

	def generate_irregluar_polygon(self,l):
		nose = []
		xs = [self.x + cos(radians(a['angle'])) * a['radio'] for a in l]
		ys = [self.y - sin(radians(a['angle'])) * a['radio'] for a in l]
		for x,y in zip(xs,ys):
			nose.append(list((x,y)))
		return nose

	def import_file(self, path):
		string = [{'angle':float(a), 'radio':float(s)} for a,s in [x.split(',') for x in open(Path(__file__).parent.joinpath(f'./figuras{path}'),'r').read().split('|')]]
		self.figure = [(self.pos.x + cos(radians(l['angle'] + self.angle))*self.radio*l['radio'],self.pos.y - sin(radians(l['angle'] + self.angle)) * self.radio*l['radio']) for l in string]

	def __str__(self):
		return f'Poligono irregular tipo={self.type} en={self.pos} angulo={self.angle}'
	
