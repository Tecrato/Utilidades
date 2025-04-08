from urllib.error import HTTPError, URLError

def errors_handler(req):
    if isinstance(req,URLError):
        raise InternetError()
    elif not isinstance(req,HTTPError):
        raise req
    if req.code == 404:
        raise UrlPerdida(req.url)
    elif req.code == 403:
        raise UrlNoAccesible(req.url)
    else:
        raise req
        # raise ErrorNoImplementado(req.url, req.code)

class UrlPerdida(Exception):
    def __init__(self, url):
        super().__init__(f"La URL no existe mas")
    

class UrlNoAccesible(Exception):
    def __init__(self, url):
        super().__init__(f"La URL no es accesible")
    

class ErrorNoImplementado(Exception):
    def __init__(self, url, code):
        super().__init__(f"Error no implementado para el codigo {code}: url[{url}]")
    

class InternetError(Exception):
    def __init__(self):
        super().__init__(f"Error con el internet")
