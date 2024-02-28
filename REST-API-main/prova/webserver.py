from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import json

class WebRequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/vnd.api+json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_response()
            response = {
                "data": {"type": "response", "attributes": {"method": "GET"}}
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self._set_response(201)
            response = {
                "data": {"type": "response", "attributes": {"method": "POST", "data": data}}
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_PUT(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            data = json.loads(put_data.decode('utf-8'))
            self._set_response(200)
            response = {
                "data": {"type": "response", "attributes": {"method": "PUT", "data": data}}
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_PATCH(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = json.loads(patch_data.decode('utf-8'))       
            self._set_response(200)
            response = {
                "data": {"type": "response", "attributes": {"method": "PATCH", "data": data}}
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_DELETE(self):
        if self.path == '/':
            self._set_response(204)

if __name__ == "__main__":
    server_address = ('localhost', 8000)
    server = HTTPServer(server_address, WebRequestHandler)
    server.serve_forever()
