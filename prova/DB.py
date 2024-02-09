import mysql.connector

mydb = mysql.connector.connect(
    host ="localhost",
    user = "user1"
    password = "123"
)

print(mydb)