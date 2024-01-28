import time
from dataclasses import dataclass,field


@dataclass
class Deltatime:
	dt:int = field(default=0,init=False,compare=False)
	FPS:int = 60

	def __post_init__(self) -> None:
		self.last_time = time.time()


	def update(self) -> None:
		self.dt = (time.time()-self.last_time) * self.FPS
		self.last_time = time.time()
		if self.dt > 5:
			self.dt = 1
	def reset(self) -> None:
		self.last_time = time.time()
		self.dt = (time.time()-self.last_time) * self.FPS
		

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
