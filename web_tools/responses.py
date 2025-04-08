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
    
    def read(self, bytes: int = 0):
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
    
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.response.close()
    def __del__(self):
        self.close()