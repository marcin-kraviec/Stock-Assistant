import mysql.connector


class DatabaseConnector():
    database = mysql.connector.connect(host='127.0.0.1', user='root', password='root',
                                       auth_plugin='mysql_native_password')
    #database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='stock_assistant', auth_plugin='mysql_native_password')
    #create_query = 'CREATE TABLE ' + str(name) + ' (id int AUTO_INCREMENT, stock varchar(250) NOT NULL, amount int NOT NULL), PRIMARY KEY (id)'

    @staticmethod
    def create_portfolio(name):
        query = 'SHOW DATABASES'
        #query = 'CREATE TABLE ' + str(name) + ' (id int AUTO_INCREMENT, stock varchar(250) NOT NULL, amount int NOT NULL), PRIMARY KEY (id)'
        cursor = DatabaseConnector.database.cursor()
        cursor.execute(query)
        for name in cursor:
            print(name)

    @staticmethod
    def insert_into_porfolio(name, stock, amount):
        pass
        #query = 'INSERT INTO ' + str(name) + ' (stock, amount) VALUES (' + str(stock) + ' ,' + str(amount) + ')'
        #cursor = DatabaseConnector.database.cursor()
        #cursor.execute(query)



