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
    
    @property
    def headers(self):
        return self.response.info()
    
    @property
    def reason(self):
        return self.response.reason
    
    @property
    def text(self):
        return self.response.read().decode('utf-8')