import mysql.connector

database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='stock_assistant')

cursor = database.cursor()

#cursor.execute("SHOW DATABASES")

class DatabaseConnector():

    database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='stock_assistant')

    def __init__(self):
        pass



