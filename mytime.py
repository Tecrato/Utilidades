import time
from dataclasses import dataclass,field

@dataclass
class Deltatime:
	dt:int = field(default=0,init=False,compare=False)
	FPS:int = 60
	smothfix:int = 5

	def __post_init__(self) -> None:
		self.last_time = time.time()


	def update(self) -> None:
		self.dt = (time.time()-self.last_time) * self.FPS
		self.last_time = time.time()
		if self.dt > self.smothfix:
			self.dt = 1
	def reset(self) -> None:
		self.last_time = time.time()
		self.dt = 0
		

def tener_el_tiempo(func):
	def wr(*args, **kwargs) -> None:
		time1 = time.perf_counter()

		result = func(*args,**kwargs)

		tiempo_final = time.perf_counter() - time1
		if tiempo_final < 1.0:
			tiempo_final *= 1000
			print(f'El tiempo fue {tiempo_final:.3f} ms')
		else:
			print(f'El tiempo fue {tiempo_final:.3f} seg')
		return result
	return wr

def format_date(seconds,escalones=5):
	result = {'seg':0,'min':0,'hour':0,'day':0,'year':0}
	if 5 < escalones < 1:
		raise Exception('Debe tener minimo 1 escalon (segundos) y un maximo de 5 (años)')
	result['seg'] = int(seconds % 60)
	if escalones > 1:
		seconds -= result['seg']
		seconds /= 60
		result['min'] = int(seconds % 60)
	if escalones > 2:
		seconds -= result['min']
		seconds /= 60
		result['hour'] = int(seconds % 24)
	if escalones > 3:
		seconds -= result['hour']
		seconds /= 24
		result['day'] = int(seconds % 365)
	if escalones > 4:
		seconds -= result['day']
		seconds /= 365
		result['year'] = int(seconds)
	return result
	