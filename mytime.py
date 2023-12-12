import time
class Deltatime:
	def __init__(self,FPS:int=60):
		self.last_time = time.time()
		self.dt = 0
		self.FPS = FPS

	def update(self):
		self.dt = (time.time()-self.last_time) * self.FPS
		self.last_time = time.time()
		if self.dt > 5:
			self.dt = 1
	def reset(self):
		self.last_time = time.time()
		self.dt = (time.time()-self.last_time) * self.FPS

def tener_el_tiempo(func):
	def wr(*args, **kwargs):
		time1 = time.pref_counter()

		func()

		tiempo_final = time.pref_counter() - time1
		print(f'El tiempo fue {tiempo_final}')
	return wr
