from threading import Thread

class Funcs_pool:
    def __init__(self) -> None:
        self.threads: dict = dict()
        self.running: dict = dict()
        self.running_ids: dict = dict()
        
    def add(self,alias: str, *funcs) -> None:
        if alias in self.threads: raise Exception('Ya existe la key')
        self.threads[f'{alias}'] = {'funcs': funcs}
        self.running[f'{alias}'] = {}
        self.running_ids[f'{alias}'] = []

    def join(self,alias, timeout=0) -> None:
        self.running[f'{alias}'][f'{self.running_ids[f'{alias}'][0]}'].join(timeout)
        self.running_ids[f'{alias}'].pop(0)
    
    def stop(self,alias):
        self.running[f'{alias}'][f'{self.running_ids[f'{alias}'][0]}'].join(0.01)
        self.running_ids[f'{alias}'].pop(0)

    def start(self,alias) -> None:
        self.go(alias)

    def go(self,alias, id=0) -> None:
        if f'{id}' in self.running_ids[f'{alias}']: return self.go(alias,id+1)
        # self.running[f'{alias}_{id}'] = Thread(target=self.new,args=(alias,id))
        # self.running[f'{alias}_{id}'].start()
        self.running_ids[f'{alias}'].append(id)
        self.running[f'{alias}'][f'{id}'] = Thread(target=self.new,args=(alias,id), daemon=True)
        self.running[f'{alias}'][f'{id}'].start()

    def new(self,alias, id) -> None:
        for f in self.threads[f'{alias}']['funcs']:
            f()
        self.running[f'{alias}'].pop(f'{id}')
        self.running_ids[f'{alias}'].remove(id)
    