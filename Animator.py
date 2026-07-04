import time
from typing import TypedDict

class Animation_Future(TypedDict):
    func: callable
    init_time: float
    time_elapsed: float
    delay: float
    repetitions: int
    times_executed: int

class Animator:
    def __init__(self):
        self.list_funcs: list[Animation_Future] = []

    def add_animation(self, func, delay: float, repetitions: int = 1):
        self.list_funcs.append({"func": func, "init_time": time.time(), "time_elapsed": 0, "delay": delay, "times_executed": 0, "repetitions": repetitions})

    def update(self, dt: float):
        to_del = []
        for i,func_dict in enumerate(self.list_funcs):
            func_dict["time_elapsed"] += dt
            if func_dict["time_elapsed"] >= func_dict["delay"]:
                func_dict["func"]()
                func_dict["time_elapsed"] -= func_dict["delay"]
                func_dict["times_executed"] += 1
                if func_dict["repetitions"] <= func_dict["times_executed"]:
                    to_del.append(i)

        for i in to_del:
            self.list_funcs.pop(i)

    def clear(self):
        self.list_funcs.clear()