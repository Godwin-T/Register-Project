import mysql.connector
import tensorflow as tf
import numpy as np

class Database:

    def __init__(self, hostname, username, password):

        self.host = hostname
        self.user = username
        self.password = password


    def create_db(self, dbname = None):
        
        if dbname !=  None:
            mydb = mysql.connector.connect( host = self.host,
                                            user = self.user,
                                            passwd = self.password,
                                            )
            cursor = mydb.cursor()
            cursor.execute(f"CREATE DATABASE {dbname}")
            print('Database Created successfully')

    def connect_db(self, dbname = None):
        mydb = mysql.connector.connect( host = self.host,
                                        user = self.user,
                                        passwd = self.password,
                                        database = dbname
                                        )
        return mydb
  

    def create_table(self, name, features, database):

       # self.database = database
        connection = self.connect_db(database)
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE {name} {features}")
        print('Table created succeccfully')