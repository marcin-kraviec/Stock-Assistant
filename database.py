import mysql.connector

class DatabaseConnector():

    #database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', auth_plugin='mysql_native_password')
    database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='stock_assistant', auth_plugin='mysql_native_password')

    @staticmethod
    def create_table(name):

        query = 'CREATE TABLE IF NOT EXISTS %s (id INT AUTO_INCREMENT PRIMARY KEY, stock VARCHAR(250) NOT NULL, amount INT NOT NULL)' % name
        print(query)

        #TODO: exception needs to be specified

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)


    @staticmethod
    def insert_into(name, key, value, flag):

        if flag == 'elements':
            query = 'INSERT INTO %s (stock, amount) VALUES (%s, %s)' % (name, key, value)
            print(query)
        if flag == 'names':
            query = 'INSERT INTO %s (name, date) VALUES (%s, %s)' % (name, key, value)
            print(query)

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            DatabaseConnector.database.commit()
        except Exception as e:
            print(e)


    @staticmethod
    def select_from(name):
        query = 'SELECT stock, amount FROM %s' % name
        print(query)

        dict = {}

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            for element in cursor:
                # tuple unpacking
                (key, value) = element
                dict[key] = value
            return dict
        except Exception as e:
            print(e)


    @staticmethod
    def drop_table(name):
        query = 'DROP TABLE %s' % name
        print(query)
        '''
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            DatabaseConnector.database.commit()
        except Exception as e:
            print(e)
        '''

    @staticmethod
    def show_tables():
        query = 'SHOW TABLES'
        print(query)
        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            names = []
            for name in cursor:
                # tuple unpacking
                (n, ) = name
                names.append(n)

            return names

        except Exception as e:
            print(e)







