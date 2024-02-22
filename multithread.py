from threading import Thread

class Funcs_pool:
    def __init__(self) -> None:
        self.threads: dict = dict()
        self.running: dict = dict()
        
    def add(self,alias: str, *funcs) -> None:
        if alias in self.threads: raise Exception('Ya existe la key')
        self.threads[f'{alias}'] = {'funcs': funcs}

    def join(self,alias, timeout=0) -> None:
        self.running[f'{alias}'].join(timeout)

    def start(self,alias) -> None:
    #     self.threads[f'{alias}']['func'].start()
        self.go(alias)

    def go(self,alias, id=0) -> None:
        if f'{alias}_{id}' in self.running: return self.go(alias,id+1)
        self.running[f'{alias}_{id}'] = Thread(target=self.new,args=(alias,id))
        self.running[f'{alias}_{id}'].start()

    def new(self,alias, id) -> None:
        for f in self.threads[f'{alias}']['funcs']:
            f()
        self.running.pop(f'{alias}_{id}')
    