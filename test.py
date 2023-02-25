import database
import register
import cv2
import keras


def create_db(database_name, host_name = 'localhost', 
              user_name = 'root', password = 'Pattern'):

    db = database.Database(host_name, user_name, password)
    db.create_db(database_name)
    print("Database Created Successfully")

def connect_db(database_name, host_name = 'localhost', user_name = 'root',
                  password = 'Pattern'):

    db = database.Database(host_name, user_name, password)
    db.connect_db(database_name)
    print("Successfully connected to Database")

def create_table(table_name, variables, database_name,
                  host_name = 'localhost', user_name = 'root',
                  password = 'Pattern'):

    db = database.Database(host_name, user_name, password)
    db.create_table(name = table_name, features = variables, database = database_name)
    print(f'{table_name} table successfully created')
  


#Create Workers information Table
name = "Workers Information"
variables = "(id int not null, name varchar(50), gender char(6), address varchar(30),\
                position varchar(20), employment_date date, resumption_date date,\
                salary_per_hr float, daily_work_hrs int, primary key (id))"
database_name = "Dark"


create_table(name, variables, database_name)

#Create register Table
name = 'Register'
variables = "(id int not null, date date, name varchar(50), \
                     time_in time, time_out time)"
create_table(name, variables, database_name)




