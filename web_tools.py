import requests, time
from bs4 import BeautifulSoup
from urllib.parse import quote, urlparse, unquote
from threading import Thread
from pathlib import Path


def check_update(program_name:str,version_actual:str,version_deseada='last'):
    response = requests.get(f'https://tecrato.pythonanywhere.com/api/programs?program={quote(program_name)}&version={quote(version_deseada)}', timeout=30)

    resultado = response.json()
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

def get_mediafire_url(url):
    a = requests.get(url, allow_redirects=True,timeout=20,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}).content
    print(a)
    soup = BeautifulSoup(a, 'html.parser')
    print(soup)
    try:
        link = soup.find(id='downloadButton').get('href',False)
        print(link)
        return link
    except:
        return False



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

        self.progress_func = progress_func
        self.session = requests.Session()

    def prepare(self):
        self.can_download = False

        parse = urlparse(self.url)
        if (parse.netloc == "www.mediafire.com" or parse.netloc == ".mediafire.com") and 'file' in parse.path:
            for x in parse.path[1:].split('/'):
                if '.' in x:
                    self.file = x
                    break
            self.url = get_mediafire_url(self.url)
            
        response = self.session.head(self.url, allow_redirects=True, stream=True, timeout=30,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'})
        self.headers = response.headers
        
        if self.file == None:
            self.file: str = parse.path
            self.file: str = self.file.split('/')[-1]
            self.file: str = self.file.replace('+', ' ')
            self.file: str = unquote(self.file) if '%' in self.file else self.file

        if 'bytes' not in response.headers.get('Accept-Ranges', ''):
            self.threads = 1
            self.resume = False
    
        self.type = response.headers.get('Content-Type', 'unknown/Nose').split(';')[0]
        if self.type in ['text/plain', 'text/html']:
            print(response.headers)
            raise Exception('No paginas')
        
        self.size = int(response.headers.get('content-length', 1))
        if self.size < self.chunk_size * self.threads:
            print(response.text)
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
            response = self.downloader.session.get(self.downloader.url, headers=headers, stream=True, timeout=30)
            with open(self.downloader.path/self.downloader.file, "+rb") as file:
                seek =self.inicio+self.progress if self.downloader.resume else 0
                file.seek(seek)
                self.sleep = 0
                for chunk in response.iter_content(chunk_size=self.downloader.chunk_size):
                    if not chunk: # filter out keep-alive new chunks
                        continue
                    if self.downloader.is_canceled:
                        break
                    file.write(chunk)
                    self.progress += len(chunk)
                    self.downloader.progress += len(chunk)
        except Exception as err:
            print(f"Error de lectura en el hilo {self.index}: {err}")
            # self.intentos += 1
            # if self.intentos < 5:
            self.sleep += 1
            if self.sleep > 3:
                self.sleep = 3
            time.sleep(self.sleep)
            self.download()
            # else:
            #     print(f"Se han agotado los intentos para el hilo {self.index}.")
