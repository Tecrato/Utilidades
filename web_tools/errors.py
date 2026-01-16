from urllib.error import HTTPError, URLError

def errors_handler(req):
    if not isinstance(req,HTTPError):
        raise req
    if isinstance(req,URLError) and not isinstance(req,HTTPError):
        raise InternetError(req)
    if req.code == 404:
        raise UrlPerdida(req.read())
    elif req.code == 403:
        raise UrlNoAccesible(req.read())
    elif req.code == 400:
        raise BadRequestError(req.read())
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
    def __init__(self, txt="Error con el internet"):
        super().__init__(txt)

class BadRequestError(Exception):
    def __init__(self, txt="Error en la peticion"):
        super().__init__(txt)

    