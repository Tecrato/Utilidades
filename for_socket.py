import socket
import time
from threading import Thread, Lock, Event
from typing import Optional, Callable

class Socket_Server_Threaded:
    def __init__(self, on_receive: Callable = None):
        self.host: Optional[str] = None
        self.port: Optional[int] = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.on_receive = on_receive
        self.threads = []
        self.running = True
        self.lock = Lock()
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.socket.close()
        except:
            pass
            
        with self.lock:
            for thread in self.threads[:]:
                try:
                    thread.join(0.1)
                    if not thread.is_alive():
                        self.threads.remove(thread)
                except:
                    pass
    
    def create_connection(self, host: str, port: int):
        self.running = True
        try:
            self.close()
            time.sleep(0.1)  # Esperar a que el socket se libere
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(60)
        except Exception as e:
            print(f"Error creando socket: {e}")
            raise
            
        self.host = host
        self.port = port
        try:
            self.socket.bind((host, port))
            self.socket.listen(5)
            print(f"Servidor escuchando en {host}:{port}")
        except Exception as e:
            print(f"Error al enlazar/escuchar: {e}")
            self.close()
            raise
        
        accept_thread = Thread(target=self.accept, daemon=True)
        accept_thread.start()
        self.threads.append(accept_thread)

    def accept(self):
        while self.running:
            try:
                client, address = self.socket.accept()
                client.settimeout(60)
                print(f"Nueva conexión desde {address}")
                thread = Thread(target=self.main_loop, args=(client,), daemon=True)
                thread.start()
                with self.lock:
                    self.threads.append(thread)
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error en accept: {e}")
                    time.sleep(1)
                continue

    def main_loop(self, client: socket.socket):
        try:
            while self.running:
                try:
                    data = self.recv(client)
                    if not data:
                        break
                        
                    if self.on_receive:
                        self.on_receive(data)
                    self.send(client, b'ok')
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error en main_loop: {e}")
                    break
        finally:
            try:
                client.shutdown(socket.SHUT_RDWR)
            except:
                pass
            try:
                client.close()
            except:
                pass
            with self.lock:
                if Thread.current_thread() in self.threads:
                    self.threads.remove(Thread.current_thread())

    def send(self, client: socket.socket, data: bytes) -> bool:
        try:
            client.sendall(data)
            return True
        except Exception as e:
            print(f"Error al enviar: {e}")
            return False

    def recv(self, client: socket.socket) -> bytes:
        try:
            data = client.recv(4096)
            if not data:
                return b''
            return data
        except Exception as e:
            print(f"Error al recibir: {e}")
            return b''

class Socket_Client:
    def __init__(self, on_receive: Callable = None):
        self.host: Optional[str] = None
        self.port: Optional[int] = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.on_receive = on_receive
        self.running = True
        self.receive_thread: Optional[Thread] = None
        self.response_ready = Event()
        self.last_response = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        self.running = False
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        try:
            self.socket.close()
        except:
            pass
        
        if self.receive_thread:
            try:
                self.receive_thread.join(0.1)
            except:
                pass
    
    def connect(self, host: str, port: int) -> bool:
        try:
            self.close()
            time.sleep(0.1)  # Esperar a que el socket se libere
            self.running = True
            self.host = host
            self.port = port
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(10)
            print(f"Intentando conectar a {host}:{port}...")
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(60)
            print("¡Conexión establecida!")
            
            self.receive_thread = Thread(target=self.main_loop, daemon=True)
            self.receive_thread.start()
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            self.close()
            return False

    def main_loop(self):
        try:
            while self.running:
                try:
                    data = self.recv()
                    if not data:
                        break
                        
                    if self.on_receive:
                        self.on_receive(data)
                    
                    # Señalizar que hay una respuesta disponible
                    self.last_response = data
                    self.response_ready.set()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error en main_loop: {e}")
                    break
        finally:
            self.close()
        
    def send(self, data: bytes) -> bool:
        try:
            # Limpiar cualquier señal anterior
            self.response_ready.clear()
            self.last_response = None
            
            # Enviar datos
            self.socket.sendall(data)
            return True
        except Exception as e:
            print(f"Error al enviar: {e}")
            return False

    def recv(self) -> bytes:
        try:
            data = self.socket.recv(4096)
            if not data:
                return b''
            return data
        except Exception as e:
            print(f"Error al recibir: {e}")
            return b''
