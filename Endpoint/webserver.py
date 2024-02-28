from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import json
import DB
import product

class WebRequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/vnd.api+json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self):
        if self.path == '/products':
            products = DB.get_all() 
            self._set_response()
            data = {"data": []}
            for product in products:
                data["data"].append({"type": "products", "id": str(product[0]), "attributes": {"marca": product[3], "nome": product[1], "prezzo": str(product[2])}})
            self.wfile.write(json.dumps(data).encode('utf-8'))
        
        elif self.path.startswith('/products/'):
            product_id = int(self.path.split('/')[-1])
            product = DB.get_by_id(product_id)
            if product:
                self._set_response()
                data = {"data": {"type": "products", "id": str(product[0]), "attributes": {"marca": product[3], "nome": product[1], "prezzo": str(product[2])}}}
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self._set_response(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            new_product_id = DB.insert_product(data['attributes']['marca'], data['attributes']['nome'], data['attributes']['prezzo'])
            self._set_response(201)
            response = {
                "data": {"type": "products", "id": str(new_product_id), "attributes": data['attributes']}
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))
    
    def do_PATCH(self):
        if self.path.startswith('/products/'):
            product_id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = json.loads(patch_data.decode('utf-8'))
            success = DB.update_product(product_id, data['attributes'])
            if success:
                self._set_response(200)
                response = {
                    "data": {"type": "products", "id": str(product_id), "attributes": data['attributes']}
                }
            else:
                self._set_response(404)
                response = {"error": "Product not found"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/products/'):
            product_id = int(self.path.split('/')[-1])
            success = DB.delete_product(product_id)
            if success:
                self._set_response(204)
            else:
                self._set_response(404)
                self.wfile.write(json.dumps({"error": "Product not found"}).encode('utf-8'))
        else:
            self._set_response(404)
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode('utf-8'))


if __name__ == "__main__":
    server_address = ('localhost', 8000)
    server = HTTPServer(server_address, WebRequestHandler)
    server.serve_forever()
