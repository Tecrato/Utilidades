from functools import wraps

CACHE_LIMIT = 3000
def memosize(funcion):
    cache = {}
    @wraps(funcion)
    def wrapper(*args,**kwargs):
        key = funcion.__name__ + str(args) + str(kwargs)
        l = len(cache)
        if l >= CACHE_LIMIT:
            cache.clear()
        if key not in cache:
            cache[key] = funcion(*args, **kwargs)
        return cache[key]
    return wrapper

