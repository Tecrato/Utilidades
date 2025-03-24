import time
import urllib.request
import http.client
import urllib.parse
import json
from typing import Dict
from http import cookiejar
from urllib.parse import quote, urlparse, unquote
from threading import Thread, Lock
from pathlib import Path
from ..logger import debug_print
from .responses import Response

DEFAULT_HEADERS: dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
}

def get(url, timeout=10, params=None) -> Response:
    """
    Retorna un Response de un url response
    
    Argumentos:
        url (str): El url el que se obtendra el response
        timeout (int, optional): El tiempo limite para la peticion. Defaults to 10.
        params (dict, optional): Los parametros para la peticion. Defaults to None.
    
    Returns:
        Response: El response
    """
    if params:
        url += '?' + urllib.parse.urlencode(params, doseq=True)
    r = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    return Response(urllib.request.urlopen(r, timeout=timeout))


def send_post(url, data: dict, timeout=10) -> dict:
    r = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={**DEFAULT_HEADERS, 'Content-Type': 'application/json'}, method='POST')
    return Response(urllib.request.urlopen(r, timeout=timeout))

def download_file(url, timeout=10, headers: dict = None, params: dict = None, stream: bool = False, **kwargs) -> Response|http.client.HTTPResponse:
    """
    Retorna un Response de un url response
    
    Argumentos:
        url (str): El url el que se obtendra el response
        timeout (int, optional): El tiempo limite para la peticion. Defaults to 10.
        headers (dict, optional): Los headers para la peticion. Defaults to None.
        params (dict, optional): Los parametros para la peticion. Defaults to None.
        stream (bool, optional): Si es True, retorna un HTTPResponse. Defaults to False.
        **kwargs: Argumentos adicionales para la peticion.
    
    Returns:
        Response|http.client.HTTPResponse: El response
    """
    if params:
        url += '?' + urllib.parse.urlencode(params, doseq=True)
    r = urllib.request.Request(url, headers=headers if headers else DEFAULT_HEADERS, **kwargs)
    if stream:
        return urllib.request.urlopen(r, timeout=timeout)
    return Response(urllib.request.urlopen(r, timeout=timeout)).data


def check_update(program_name:str,version_actual:str,version_deseada='last'):
    """
    Retorna un diccionario con la version mas reciente y url del programa
    
    Argumentos:
        program_name (str): El nombre del programa
        version_actual (str): La version actual del programa
        version_deseada (str, optional): La version a verificar. Defaults to 'last'.
    
    Returns:
        dict: La version mas reciente y url del programa
    """
    resultado = get(f'https://tecrato.pythonanywhere.com/api/programs?program={quote(program_name)}&version={quote(version_deseada)}', timeout=30).json

    if resultado['status'] == 'error':
        return False
    version_actual = version_actual.split('.')
    version_internet = resultado['version'].split('.')
    cuenta_versiones = max(len(version_actual),len(version_internet))

    for x in range(cuenta_versiones):
        version_actual.append(0)
        version_internet.append(0)
        if int(version_internet[x]) > int(version_actual[x]):
            return {'version': resultado['version'], 'url': resultado['url']}
        elif int(version_internet[x]) < int(version_actual[x]):
            return False
    else:
        return False

class Http_Session:
    def __init__(self):
        self.session = cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.session),urllib.request.HTTPHandler())
        self.__headers = {'User-Agent': 'Mozilla/5.0'}
    
    def head(self, url, timeout=10, headers: dict = None, **kwargs) -> dict:
        r = urllib.request.Request(url, headers=headers if headers else self.__headers, **kwargs)
        with self.opener.open(r, timeout=timeout) as response:
            return response.info()

    def get(self, url, timeout=10, stream: bool = False, headers: dict = None, params: dict = None, **kwargs) -> Response | http.client.HTTPResponse | None:
        if params:
            url += '?' + urllib.parse.urlencode(params, doseq=True)
        try:
            r = urllib.request.Request(url, headers=headers if headers else self.__headers, **kwargs)
            if stream:
                return self.opener.open(r, timeout=timeout)
            return Response(self.opener.open(r, timeout=timeout))
        except urllib.error.HTTPError as e:
            print(f"Error HTTP {e.code}: {e.reason}")
            return None
    
    def post(self, url, data: dict, timeout=10, headers: dict = None, **kwargs) -> dict:
        r = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers if headers else self.__headers, method='POST', **kwargs)
        with self.opener.open(r, timeout=timeout) as response:
            el_read = response.read()
            return {'headers': response.info(), 'data': json.loads(el_read.decode('utf-8'))}

    def download_file(self, url, timeout=10, headers: dict = None, params: dict = None, **kwargs) -> http.client.HTTPResponse:
        """
        response = clase.download_file(url, timeout, headers, params, **kwargs)
        while True:
            chunk = response.read(1024)
            if not chunk:
                break
            logic

        """
        if params:
            url += '?' + urllib.parse.urlencode(params, doseq=True)
        r = urllib.request.Request(url, headers=headers if headers else self.__headers, **kwargs)
        return self.opener.open(r, timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def cookies(self) -> Dict[str, str]:
        return {cookie.name: cookie.value for cookie in self.session}

    @cookies.setter
    def cookies(self, cookies: Dict[str, str]) -> None:
        # Set cookies from dict (simplificado)
        for name, value in cookies.items():
            cookie = cookiejar.Cookie(
                version=0,
                name=name,
                value=value,
                port=None,
                port_specified=False,
                domain='',
                domain_specified=False,
                domain_initial_dot=False,
                path='/',
                path_specified=True,
                secure=False,
                expires=None,
                discard=False,
                comment=None,
                comment_url=None,
                rest={}
            )
            self.session.set_cookie(cookie)


    @property
    def headers(self) -> dict:
        return self.__headers

    @headers.setter
    def headers(self, headers: dict) -> None:
        self.__headers.update(headers)

    def close(self):
        """Liberar recursos de conexión"""
        self.opener.close()

class Download:
    """
    The new clas to create a download
    
    1. url: The url to download the file
    2. path: The path to save the file
    3. name: The name of the file, if not specified, it will be the name of the url
    4. threads: The number of threads to download the file, default is 4
    5. chunk_size: The size of the chunks to download the file, default is 1024
    6. progress_func: The function to call when the progress of the download changes, default is None

    Insructions to use:
     - Call the clas given 3 parameters, the url, the path and the name of the file.
     - Call the method prepare to prepare the download.
     - Call the method start to start the download.

    Warning, is experimental and not have errors watching.
    
    """
    def __init__(self,url,path,name=None, threads=4, chunk_size=1024, progress_func=None):
        self.url = url
        self.path = Path(path)
        self.size = 0
        # self.file = self.path.joinpath("./"+(name if name else url.split('/')[-1]))
        self.file = name
        self.threads = threads
        self.chunk_size = chunk_size
        self.type = None

        self.can_download = False
        self.__progress = 0
        self.is_finished = False
        self.is_canceled: bool = False
        self.resume = True

        self.list_threads_download = []
        self.thread = None
        self.write_lock = Lock()

        self.progress_func = progress_func
        self.session = Http_Session()

    def prepare(self):
        self.can_download = False

        parse = urlparse(self.url)
        
        response = self.session.head(self.url, timeout=30)
        self.headers = response
        debug_print(response)
        
        if self.headers.get('Content-Disposition'):
            self.file = self.headers.get('Content-Disposition').split('filename=')[1].strip('"')
        elif not self.file :
            self.file: str = parse.path
            self.file: str = self.file.split('/')[-1]
            self.file: str = self.file.replace('+', ' ')
            self.file: str = unquote(self.file)
        else:
            self.file = "downloaded_file"
            if self.headers.get('Content-Type'):
                self.file += "." + self.headers.get('Content-Type').split('/')[1]

        if 'bytes' not in response.get('Accept-Ranges', ''):
            self.threads = 1
            self.resume = False
    
        self.type = response.get('Content-Type', 'unknown/Nose').split(';')[0]
        if self.type in ['text/plain', 'text/html']:
            raise Exception('No paginas')
        
        self.size = int(response.get('content-length', 1))
        if self.size < self.chunk_size * self.threads:
            raise Exception('Peso muy pequeño')
        self.can_download = True
        return True
    
    def download(self):
        if not self.can_download:
            return False
        self.thread = Thread(target=self.__download,daemon=True)
        self.thread.start()
    
    def join(self, time=None):
        self.thread.join(time)

    def __download(self):
        # print(os.listdir(self.path))
        # Path(self.path).mkdir(parents=True, exist_ok=True)
        with open(self.path/self.file, 'wb') as f:
            f.truncate(self.size)

        self.list_threads_download = []
        self.progress = 0
        self.is_finished = False
        for xt in range(self.threads):
            start = xt * (self.size // self.threads)
            end = (xt + 1) * (self.size // self.threads) - 1
            if xt == self.threads - 1:  # Asegurarse de que el último hilo descargue el resto de los bytes
                end = self.size

            self.list_threads_download.append(DownloadThread(self, start, end, xt))
            self.list_threads_download[xt].start()

    def cancel(self) -> None:
        self.is_canceled = True
        for xt in self.list_threads_download:
            xt.join(1)
        self.list_threads_download: list[DownloadThread] = []


    @property
    def progress(self):
        return self.__progress
    @progress.setter
    def progress(self, value):
        self.__progress = value
        if self.progress_func is not None:
            self.progress_func(self.__progress/self.size)
        if self.__progress == self.size:
            self.is_finished = True

        
        
class DownloadThread(Thread):
    def __init__(self, downloader: Download, start: int, end: int, index: int) -> None:
        self.downloader: Download = downloader
        self.inicio: int = start
        self.end: int = end
        self.index: int = index
        self.size: int = end - start + 1
        self.progress: int = 0
        self.intentos: int = 0
        self.sleep: int = 0
        super().__init__(target=self.download, daemon=True)
    
    def download(self):
        print(f"empezo{self.index}")
        headers = {'Range': f'bytes={self.inicio+self.progress}-{self.end}','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        try:
            response = self.downloader.session.download_file(self.downloader.url, headers=headers, timeout=30)
            with open(self.downloader.path/self.downloader.file, "+rb") as file:
                seek =self.inicio+self.progress if self.downloader.resume else 0
                self.downloader.write_lock.acquire()
                file.seek(seek)
                self.downloader.write_lock.release()
                self.sleep = 0
                
                while True:
                    chunk = response.read(self.downloader.chunk_size)
                    if not chunk or self.downloader.is_canceled: # filter out keep-alive new chunks
                        break
                    self.downloader.write_lock.acquire()
                    file.write(chunk)
                    self.progress += len(chunk)
                    self.downloader.write_lock.release()
                    self.downloader.progress += len(chunk)
            response.close()
        except Exception as err:
            debug_print(f"Error de lectura en el hilo {self.index}: {err}")
            self.sleep += 1
            if self.sleep > 3:
                self.sleep = 3
            time.sleep(self.sleep)
            self.download()
