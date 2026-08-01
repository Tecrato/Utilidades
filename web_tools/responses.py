import json
import http.client
class Response:
    def __init__(self, response: http.client.HTTPResponse):
        self.response: http.client.HTTPResponse = response

    @property
    def json(self) -> dict:
        return json.loads(self.response.read().decode('utf-8'))
    
    @property
    def data(self):
        return self.response.read()
    
    def read(self, bytes: int = None):
        return self.response.read(bytes or None)
    
    @property
    def headers(self):
        return self.response.info()
    
    @property
    def reason(self):
        return self.response.reason
    
    @property
    def text(self):
        return self.response.read().decode('utf-8')

    @property
    def status(self):
        return self.response.status
    
    @property
    def status_code(self):
        return self.response.getcode()

    @property
    def length(self):
        return self.response.length
    
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.response.close()
    def __del__(self):
        self.close()

    def __str__(self):
        return f"Response(status_code={self.status}, headers={self.headers}, reason={self.reason}, length={self.response.length})"
    def __repr__(self):
        return self.__str__()