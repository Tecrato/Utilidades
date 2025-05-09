from typing import Any, Callable
import time
from threading import Thread, Lock, Condition, Timer

class Funcs_pool:
    def __init__(self) -> None:
        self.threads: dict = dict()
        self.running: dict = dict()
        self.running_ids: dict = dict()
        
    def add(self,alias: str, *funcs) -> None:
        if alias in self.threads: raise Exception('Ya existe la key')
        self.threads[f'{alias}'] = {'funcs': funcs}
        if not f'{alias}' in self.running:
            self.running[f'{alias}'] = {}
            self.running_ids[f'{alias}'] = []

    def join(self,alias, timeout=0) -> None:
        self.running[f'{alias}'][f'{self.running_ids[f'{alias}'][0]}'].join(timeout)
        # self.running_ids[f'{alias}'].pop(0)

    def stop_all(self):
        for x in self.running.keys():
            for a in range(len(self.running_ids[x])):
                self.running[f'{x}'][f'{a}'].join(0.01)
            self.running_ids[f'{x}'].clear()
    
    def stop(self,alias):
        self.running[f'{alias}'][f'{self.running_ids[f'{alias}'][0]}'].join(0.01)
        self.running_ids[f'{alias}'].pop(0)

    def start(self,alias: str) -> None:
        '''
        Inicia una secuencia de funciones guardadas segun el alias.
        '''
        if not alias in self.threads:
            raise Exception('Thread con funciones no encontrado')
        self.__go(alias)

    def __go(self, alias, id=0) -> None:
        if f'{id}' in self.running_ids[f'{alias}']:
            return self.__go(alias,id+1)
        # self.running[f'{alias}_{id}'] = Thread(target=self.new,args=(alias,id))
        # self.running[f'{alias}_{id}'].start()
        self.running_ids[f'{alias}'].append(id)
        self.running[f'{alias}'][f'{id}'] = Thread(target=self.__new,args=(alias,id), daemon=True)
        self.running[f'{alias}'][f'{id}'].start()

    def __new(self,alias, id) -> None:
        for i,f in enumerate(self.threads[f'{alias}']['funcs']):
            f()
        self.running[f'{alias}'].pop(f'{id}')
        self.running_ids[f'{alias}'].pop(id)

class Semaforo:
    def __init__(self,count=1,limit=1) -> None:
        self.count = count
        self.limit = limit
        self.lock = Lock()
        self.condition_v = Condition(self.lock)

    def acquire(self):
        with self.lock:
            while self.count > self.limit:
                self.condition_v.wait()
            self.count += 1

    def release(self):
        with self.lock:
            self.count -= 1
            self.condition_v.notify()
    
class Interval_funcs:
    def __init__(self):
        self.task_dict: dict[str,dict[str, Any]] = {}
        self.tasks_threads = {}

    def add(self, alias: str, func: Callable, time: float = 1, start = False):
        self.task_dict[alias] = {'func': func, 'time': time}
        if start:
            self.start_task(alias)
    
    def start_task(self, alias):
        alias = '{}'.format(alias)
        if self.tasks_threads.get(alias, False):
            return False
        self.tasks_threads[alias] = Thread(target=self.__start_func, args=(alias,), daemon=True)
        self.tasks_threads[alias].start()

    def __start_func(self,alias):
        time.sleep(self.task_dict[alias]['time'])
        while True:
            self.task_dict[alias]['func']()
            time.sleep(self.task_dict[alias]['time'])
    
    def change_time(self, alias: str, new_time: float):
        self.task_dict[alias]['time'] = new_time
    
    def join(self, alias: str):
        self.tasks_threads[alias].join(0.1)
        del self.tasks_threads[alias]
    
    def timer(self, alias: str, func: Callable, time: float = 1, *args, **kwargs):
        if self.tasks_threads.get(alias, False):
            raise Exception('Ya existe la key')
        self.tasks_threads[alias] = Timer(time, func, args=args, kwargs=kwargs)
        self.tasks_threads[alias].start()
        