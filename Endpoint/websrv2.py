from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qsl, urlparse
import json
import DB
import product

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            product = DB
            # Estrarre i dati dal payload della richiesta
            nome = data.get('nome')
            prezzo = data.get('prezzo')
            marca = data.get('marca')

            # Creare il prodotto nel database utilizzando il metodo insert
            DB.insert(nome, prezzo, marca)

            # Ottenere l'ID del prodotto appena creato (potrebbe essere gestito in modo diverso nel tuo database)
            new_product_id = 10  # Esempio di ID

            # Costruire la risposta JSON con i dati del prodotto appena creato
            response_data = {
                "data": {
                    "type": "products",
                    "id": str(new_product_id),
                    "attributes": {
                        "marca": marca,
                        "nome": nome,
                        "prezzo": str(prezzo)
                    }
                }
            }

            # Impostare la risposta con lo status code 201 (Created)
            self._set_response(201)
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_DELETE(self):
        parsed_path = self.path.split('/')
        if len(parsed_path) == 3 and parsed_path[1] == 'products':
            product_id = parsed_path[2]
            
            # Eseguire la query di eliminazione utilizzando il metodo delete
            DB.delete(product_id)

            # Costruire la risposta JSON confermando l'eliminazione
            response_data = {
                "data": {
                    "type": "response",
                    "attributes": {
                        "message": f"Product with ID {product_id} has been deleted"
                    }
                }
            }

            # Impostare la risposta con lo status code 200 (OK)
            self._set_response(200)
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            # Se l'URL non è conforme alle aspettative, restituire un errore 404 (Not Found)
            self._set_response(404)
            self.wfile.write("Path not found".encode('utf-8'))


    def do_PATCH(self):
        parsed_path = self.path.split('/')
        if len(parsed_path) == 3 and parsed_path[1] == 'products':
            product_id = parsed_path[2]

            # Leggere i dati dal corpo della richiesta
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Estrarre i dati che devono essere aggiornati
            nome = data.get('nome')
            prezzo = data.get('prezzo')
            marca = data.get('marca')

            # Eseguire la query di aggiornamento utilizzando il metodo patch
            DB.update(product_id, nome, prezzo, marca)

            # Costruire la risposta JSON con i dati del prodotto aggiornato
            updated_product = {
                "data": {
                    "type": "products",
                    "id": str(product_id),
                    "attributes": {
                        "marca": marca,
                        "nome": nome,
                        "prezzo": str(prezzo)
                    }
                }
            }

            # Impostare la risposta con lo status code 200 (OK)
            self._set_response(200)
            self.wfile.write(json.dumps(updated_product).encode('utf-8'))
        else:
            # Se l'URL non è conforme alle aspettative, restituire un errore 404 (Not Found)
            self._set_response(404)
            self.wfile.write("Path not found".encode('utf-8'))


    def do_GET(self):
        parsed_path = self.path.split('/')
        if parsed_path[1] == 'products':
            if len(parsed_path) == 2:
                # Se l'URL è '/products', esegui la logica per recuperare tutti i prodotti
                products = DB.get_all_products()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "data": {"type": "response", "attributes": {"method": "GET", "products": products}}
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            elif len(parsed_path) == 3:
                # Se l'URL ha un ID, esegui la logica per recuperare il prodotto con quell'ID
                product_id = parsed_path[2]
                product = DB.get_product_by_id(product_id)
                if product:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        "data": {"type": "response", "attributes": {"method": "GET", "product": product}}
                    }
                    self.wfile.write(json.dumps(response).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": {"message": "Product not found"}}
                    self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            # Gestione degli altri percorsi non gestiti
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write("Path not found".encode('utf-8'))


if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('Server running...')
    httpd.serve_forever()