import mysql.connector

class Database:

    def __init__(self, hostname, username, password, database=None):

        self.host = hostname
        self.user = username
        self.password = password
        self.database = database


    def connect_db(self):
        mydb = mysql.connector.connect( host = self.host,
                                        user = self.user,
                                        passwd = self.password,
                                        database = self.database
                                        )
        return mydb

    

    def create_db(self, name):
        connection = Database.connect_db(self)
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE {name}")
        print('Database Created successfully')

    def create_table(self, name, features, database):

        self.database = database
        connection = Database.connect_db(self)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE {name} {features}")
        print('Table created succeccfully')