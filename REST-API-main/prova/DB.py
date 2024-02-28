import mysql.connector
import json

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

def get_connection():
    config = read_config('config.txt')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return cursor, conn

if __name__ == "__main__":
    query = "SELECT * FROM rizzato_filippo_API.products"
    cursor, conn = get_connection()
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    cursor.close()
    conn.close()
    
def get_one(id):
    query = f"SELECT * FROM rizzato_filippo_API.products WHERE id = {id}"
    cursor, conn = get_connection()
    cursor.execute(query)
    cursor.fetchobject()
    cursor.close()
    conn.close()
    
def create(nome, marca, prezzo):
    query = f"INSERT INTO rizzato_filippo_API.products(nome, prezzo, marca) values({nome},{prezzo},{marca})"
    cursor, conn = get_connection()
    cursor.execute(query)
    cursor.close()
    conn.close()
    
def delete(id):
    query = f"DELETE FROM rizzato_filippo_API.products where id = {id}"
    cursor, conn = get_connection()
    cursor.execute
    cursor.close()
    conn.close()
    
json = {
"data": {
"type": "products",
"id": "10",
"attributes": {
"marca": "Nike"
}
}
}


req = json.loads(json)
req = req["data"]["attributes"]
def patch(req, id):
    query = f"UPDATE FROM rizzato_filippo_API.products where id = {id}"
    cursor, conn = get_connection()
    cursor.execute
    cursor.close()
    conn.close()
    
