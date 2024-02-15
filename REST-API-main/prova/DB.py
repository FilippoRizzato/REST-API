import mysql.connector

mydb = mysql.connector.connect(
    host ="localhost",
    user = "rizzato_filippo",
    password = " scouring.immodestys.hiding."
)

print(mydb)