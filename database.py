import mysql.connector

class DatabaseConnector():

    #database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', auth_plugin='mysql_native_password')
    #database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='stock_assistant', auth_plugin='mysql_native_password')


    @staticmethod
    def db_test(db):
        query = 'SHOW DATABASES'
        #cursor = DatabaseConnector.database.cursor()
        #cursor.execute(query)
        print(db)
        #for name in cursor:
        #    print(name)

    @staticmethod
    def create_portfolio(name):
        # PROBLEM HERE amount should be stored as varchar
        query = 'CREATE TABLE IF NOT EXISTS %s (id INT AUTO_INCREMENT PRIMARY KEY, stock VARCHAR(250) NOT NULL, amount INT NOT NULL)' % name
        print(query)

        #TODO: exception needs to be specified
        '''
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
        '''

    @staticmethod
    def insert_into_porfolio(name, stock, amount):
        query = 'INSERT INTO %s (stock, amount) VALUES (%s, %s)' % (name, stock, amount)
        print(query)
        '''
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            DatabaseConnector.database.commit()
        except Exception as e:
            print(e)
        '''



