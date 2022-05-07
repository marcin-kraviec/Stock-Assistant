import mysql.connector
import logging
import sys


class DatabaseConnector:

    # establishing connection to database
    try:
        database = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='stock_assistant',
                                           auth_plugin='mysql_native_password')
    except mysql.connector.Error as e:
        logging.critical('Connection to database has not been established: ' + str(e))
        sys.exit()

    @staticmethod
    def create_table(name):

        query = 'CREATE TABLE IF NOT EXISTS %s (id INT AUTO_INCREMENT PRIMARY KEY, stock VARCHAR(250) NOT NULL, amount FLOAT NOT NULL, value FLOAT NOT NULL, date VARCHAR(250) NOT NULL )' % name

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def insert_into(name, stock, amount, value, date):

        query = 'INSERT INTO %s (stock, amount, value, date) VALUES (%s, %s, %s, %s)' % (name, stock, amount, value, date)


        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def select_from(name):

        query = 'SELECT stock, amount, value, date FROM %s' % name

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            data = []
            for element in cursor:
                # tuple unpacking
                (stock, amount, value, date) = element
                line = [stock, amount, value, date]
                data.append(line)
            return data
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def delete_from(name, stock, date):

        query = 'DELETE FROM %s WHERE stock=%s and date=%s' % (name, stock, date)

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def drop_table(name):

        query = 'DROP TABLE %s' % name

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            DatabaseConnector.database.commit()
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

    @staticmethod
    def show_tables():

        query = 'SHOW TABLES'

        try:
            cursor = DatabaseConnector.database.cursor()
            cursor.execute(query)
            names = []
            for name in cursor:
                # tuple unpacking
                (n,) = name
                names.append(n)
            return names
        except (mysql.connector.Error, AttributeError) as e:
            logging.error('Query has not been executed: ' + str(e))

