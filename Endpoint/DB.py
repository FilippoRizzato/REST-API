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


    

def insert(nome, prezzo, marca):
    query = f"insert into rizzato_filippo_API.products(nome, prezzo, marca)values ('{nome}', {prezzo}, '{marca}')"
    cursor, conn = get_connection()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def delete(id):
    query = f"delete from rizzato_filippo_API.products where id = {id}"
    cursor, conn = get_connection()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
# creo un metodo per ogni verbo
def update(lista_chiavi, lista_valori, id):
    query = f"UPDATE rizzato_filippo_API.products SET "
    for i in range(len(lista_chiavi)):
        if (lista_chiavi[i] == "prezzo"):
            query += f"{lista_chiavi[i]} = {lista_valori[i]}"
        else:
            query += f'{lista_chiavi[i]} = "{lista_valori[i]}"'
        if (i != len(lista_chiavi)-1):
            query += ", "
    query += f" WHERE id = {id}"
    print (query)
    cursor, conn = get_connection()  
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()


    
def get_product_by_id(product_id):
    query = f"SELECT * FROM rizzato_filippo_API.products WHERE id = {product_id}"
    cursor, conn = get_connection()
    cursor.execute(query)
    product = cursor.fetchone()
    print(product)
    cursor.close()
    conn.close()
    return product
def get_all():
    query = "SELECT * FROM rizzato_filippo_API.products"
    cursor, conn = get_connection()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return  results
    
if __name__ == "__main__":
    get_product_by_id(5)
    get_all()