from datetime import datetime
import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from mtcnn.mtcnn import MTCNN


class worker():

    def __init__(self, new_connection, cursor, model):
        #super().__init__(model)
        
        self.new_connection = new_connection
        self.cursor = cursor

        self.img = self.image(model)


    class image:
     
        def __init__(self, model):
            self.model = model


        def img_to_encoding(self, img):
            img = cv2.resize(img, (160, 160))
            img = np.around(np.array(img) / 255.0, decimals=12)
            x_train = np.expand_dims(img, axis=0)
            embedding = self.model.predict_on_batch(x_train)
            return embedding / np.linalg.norm(embedding, ord=2)

        def directory_img_encoding(self,image_path):
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))
            img = np.around(np.array(img) / 255.0, decimals=12)
            x_train = np.expand_dims(img, axis=0)
            embedding = self.model.predict_on_batch(x_train)
            return embedding / np.linalg.norm(embedding, ord=2)

        
        def capture(self):
            vid = cv2.VideoCapture(0)
            
            while(True):
            
                ret, frame = vid.read()
                cv2.imshow('frame', frame)
                if cv2.waitKey(8000): #& 0xFF == ord('q'):
                    break
            vid.release()
            cv2.destroyAllWindows()
            return frame

        def extract(self, frame):
            
            detector = MTCNN()
            results = detector.detect_faces(frame)
            x1, y1, width, height = results[0]['box']
            # bug fix
            x1, y1 = abs(x1), abs(y1)
            x2, y2 = x1 + width, y1 + height
            # extract the face
            face = frame[y1:y2, x1:x2]
            # resize pixels to the model size
            image = Image.fromarray(face)
            image = image.resize((160,160))
            return image



    def register_worker(self):

        id = int(input('Enter a new id: '))
        name = str(input('Enter your name: '))
        gender = input('What is your gender: ')
        address = input('Enter you address: ')
        position = input('What is your position in the company')
        employment_date = input("Enter your employment date: ")
        resumption_date = input("Enter your resumption date: ")
        salary_per_hr = input('Enter worker hourly pay: ')
        daily_work_hrs = input('Enter work total work hours per day: ')

        record = (id, name, gender, address, position, employment_date,
                        resumption_date, salary_per_hr, daily_work_hrs)
        self.cursor.execute(f"insert into workers_info\
                        values{record}")
        self.new_connection.commit()
        print("Successully added the worker's record")

    def sign_in(self, img_database):
    
        id = int(input('Enter your id: '))
        validation = self.worker_val('workers_info', id)

        if validation =='pass':
            date = datetime.today().strftime('%Y-%m-%d')
            name = str(input('Enter your name: '))

            frame = self.img.capture()
            #img = extract(frame)
            img = np.asarray(frame)
            plt.imshow(img)
            real_worker = self.verify(img, name, img_database)

            if real_worker == True:
            
                time_in =  datetime.today().strftime('%H:%M')
                time_out = datetime.today().strftime('%H:%M')

                record = (id, date, name, time_in, time_out)
                self.cursor.execute(f"insert into register \
                            values{record}")

                self.new_connection.commit()
                print("Successully added the new record")

            else:
                print('Individual recod not in database')


    

    def worker_val(self, dbname, id):

        self.cursor.execute(f"select * from {dbname}")
        myresult = self.cursor.fetchall()
        workers_id = [x[0] for x in myresult]
        print(workers_id)
        if id in workers_id:
            return ('pass')
        else:
            reg = input('Will the worker be registered: ')
            reg = reg.lower()

            if reg=='yes':
                new_input = self.register_worker()
            else:
                print('Individual not in company database')

    def signin_val(self, dbname, id):

        date = datetime.today().strftime('%Y-%m-%d')
        self.cursor.execute(f"select * from {dbname} where date = '{date}'")
        myresult = self.cursor.fetchall()
        workers_id = [x[0] for x in myresult]

        if id in workers_id:
            print('pass')
        
        else:
            print('Individual did not sign in today')

    def sign_out(self, img_database):

        id = int(input('Enter your id: '))
        clock_out = self.signin_val('register', id)

        if clock_out=='pass':

            name = str(input('Enter your name: '))
            frame = self.img.capture()
            #img = extract(frame)
            img = np.asarray(frame)
            plt.imshow(img)
            real_worker = self.verify(img, name, img_database)

            if real_worker == True:
                    
                time = datetime.now().strftime('%H:%M')
                query = f"update register set \
                            time_out = '{time}' \
                            where id = {id}"
                self.cursor.execute(query)
                self.new_connection.commit()
                print("Successully updated the record")


    def verify(self, img, identity, database):

        encoding = self.img.img_to_encoding(img)
        dist = np.linalg.norm(database[identity] -  encoding)
        if dist < 0.7:
            return True
        else:
            return False