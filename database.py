import mysql.connector
import tensorflow as tf
import numpy as np

class Database:

    def __init__(self, hostname, username, password):

        self.host = hostname
        self.user = username
        self.password = password

    def connect_server(self):
        mydb = mysql.connector.connect( host = self.host,
                                        user = self.user,
                                        passwd = self.password,
                                        )
        return mydb

    def connect_db(self, dbname):
        mydb = mysql.connector.connect( host = self.host,
                                        user = self.user,
                                        passwd = self.password,
                                        database = dbname
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