from functools import wraps

CACHE_LIMIT = 10_000
def memosize(funcion):
    cache = {}
    @wraps(funcion)
    def wrapper(*args,**kwargs):
        key = funcion.__name__ + str(args) + str(kwargs)
        if len(cache) > CACHE_LIMIT:
            cache.clear()
            print("Limpieza de cache")
        if key not in cache:
            cache[key] = funcion(*args, **kwargs)
        return cache[key]
    return wrapper

    