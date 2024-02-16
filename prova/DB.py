import mysql.connector

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
