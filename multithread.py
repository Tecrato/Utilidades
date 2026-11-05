from typing import Any, Callable
import time
from threading import Thread, Lock, Condition, Timer, Event, current_thread

from .logger import debug_print

class Funcs_pool:
    """Lanza secuencias de funciones en hilos, una ejecución por alias e id.

    `running[alias]` guarda los hilos vivos con clave `str(id)` y
    `running_ids[alias]` los ids (int) en uso, así que un id no se reutiliza
    mientras su hilo siga vivo.
    """

    def __init__(self) -> None:
        self.threads: dict = dict()
        self.running: dict = dict()
        self.running_ids: dict = dict()
        self.lock = Lock()
        
    def add(self,alias: str, *funcs, daemon=True) -> None:
        if alias in self.threads: raise Exception('Ya existe la key')
        self.threads[f'{alias}'] = {'funcs': funcs, 'daemon':  daemon}
        with self.lock:
            self.running.setdefault(f'{alias}', {})
            self.running_ids.setdefault(f'{alias}', [])

    def join(self,alias, timeout: float|None = None) -> None:
        """Espera a que terminen todas las ejecuciones vivas del alias."""
        with self.lock:
            hilos = list(self.running.get(f'{alias}', {}).values())
        for hilo in hilos:
            hilo.join(timeout)

    def stop_all(self, timeout: float|None = None) -> None:
        """Espera a que terminen todos los hilos.

        No puede matar una función bloqueada: si con `timeout` alguna sigue
        viva, se queda registrada y se puede volver a esperar.
        """
        with self.lock:
            aliases = list(self.running)
        for alias in aliases:
            self.join(alias, timeout)
    
    def stop(self,alias, timeout: float|None = None) -> None:
        self.join(alias, timeout)

    def start(self,alias: str) -> None:
        '''
        Inicia una secuencia de funciones guardadas segun el alias.
        '''
        alias = f'{alias}'
        if not alias in self.threads:
            raise Exception('Thread con funciones no encontrado')
        self.__go(alias)

    def __go(self, alias) -> None:
        with self.lock:
            ids = set(self.running_ids[alias])
            id = 0
            while id in ids:
                id += 1
            hilo = Thread(target=self.__new,args=(alias,id), daemon=self.threads[alias]['daemon'])
            self.running_ids[alias].append(id)
            self.running[alias][f'{id}'] = hilo
        hilo.start()

    def __new(self,alias, id) -> None:
        try:
            for f in self.threads[f'{alias}']['funcs']:
                f()
        finally:
            # Borra solo su entrada: si el hilo se reinició, el id ya es de otro.
            with self.lock:
                if self.running[f'{alias}'].get(f'{id}') is current_thread():
                    del self.running[f'{alias}'][f'{id}']
                    if id in self.running_ids[f'{alias}']:
                        self.running_ids[f'{alias}'].remove(id)

class Semaforo:
    """Semaforo de conteo: `count` permisos libres, `limit` el máximo posible.

    Semaforo(1, 1) es binario: el primer acquire pasa y el segundo espera a un
    release(). Nunca se supera `limit`: liberar de más lanza ValueError en vez
    de dejar el contador corrupto.
    """
    def __init__(self,count=1,limit=1) -> None:
        self.limit = max(1, int(limit))
        self.count = min(max(0, int(count)), self.limit)
        self.lock = Lock()
        self.condition_v = Condition(self.lock)

    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        with self.condition_v:
            if not blocking and self.count == 0:
                return False
            if not self.condition_v.wait_for(lambda: self.count > 0, timeout if timeout >= 0 else None):
                return False
            self.count -= 1
            return True

    def release(self) -> None:
        with self.condition_v:
            if self.count >= self.limit:
                raise ValueError('Semaforo liberado más veces de las permitidas')
            self.count += 1
            self.condition_v.notify()
    
class Interval_funcs:
    """Ejecuta una función cada `time` segundos, con parada limpia."""

    def __init__(self):
        self.task_dict: dict[str,dict[str, Any]] = {}
        self.tasks_threads = {}

    def add(self, alias: str, func: Callable, time: float = 1, start = False):
        alias = '{}'.format(alias)
        if alias in self.task_dict:
            raise AttributeError("Alias en uso")
        self.task_dict[alias] = {'func': func, 'time': time, 'stop': Event()}
        if start:
            self.start_task(alias)
    
    def start_task(self, alias):
        alias = '{}'.format(alias)
        if self.task_dict.get(alias) is None:
            raise KeyError('Intervalo no encontrado')
        hilo = self.tasks_threads.get(alias)
        if hilo is not None and hilo.is_alive():
            return False
        stop = Event()
        self.task_dict[alias]['stop'] = stop
        self.tasks_threads[alias] = Thread(target=self.__start_func, args=(alias, stop), daemon=True)
        self.tasks_threads[alias].start()
        return True

    def __start_func(self, alias, stop: Event):
        # stop.wait(t) duerme el intervalo y despierta al instante si se pide parar.
        # Si la función lanza, el intervalo sigue vivo: el hilo no puede morir
        # en silencio dejando el objeto como si estuviera funcionando.
        while not stop.wait(self.task_dict[alias]['time']):
            try:
                self.task_dict[alias]['func']()
            except Exception as exc:
                debug_print(f'intervalo {alias!r} lanzó {type(exc).__name__}: {exc}', priority=3)
    
    def change_time(self, alias: str, new_time: float):
        self.task_dict['{}'.format(alias)]['time'] = new_time

    def stop_task(self, alias: str) -> bool:
        """Pide al intervalo que termine; el hilo sale en la siguiente espera."""
        tarea = self.task_dict.get('{}'.format(alias))
        if tarea is None:
            return False
        tarea['stop'].set()
        return True
    
    def join(self, alias: str, timeout: float|None = None) -> bool:
        """Detiene el intervalo y espera a que su hilo termine. True si terminó."""
        alias = '{}'.format(alias)
        self.stop_task(alias)
        hilo = self.tasks_threads.get(alias)
        if hilo is None:
            return False
        hilo.join(timeout)
        if hilo.is_alive():
            return False
        del self.tasks_threads[alias]
        return True
    
    def timer(self, alias: str, func: Callable, time: float = 1, *args, **kwargs):
        """Ejecuta `func` una sola vez dentro de `time` segundos."""
        alias = '{}'.format(alias)
        hilo = self.tasks_threads.get(alias)
        if hilo is not None and hilo.is_alive():
            raise Exception('Ya existe la key')
        self.tasks_threads[alias] = Timer(time, func, args=args, kwargs=kwargs)
        self.tasks_threads[alias].start()
        