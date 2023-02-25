import database
import register
import cv2
import keras


def connect_db(database_name, host_name = 'localhost', user_name = 'root',
                  password = 'Pattern'):

    db = database.Database(host_name, user_name, password)
    db.connect_db(database_name)
    print("Successfully connected to Database")

def model(path, classifier_path):
    frmodel = keras.models.load_model(path)
    classifier = cv2.CascadeClassifier(classifier_path)
    return frmodel, classifier

#Connect to database
database_name = "DARK"
new_connection = connect_db(database_name)
cursor = new_connection.cursor(buffered=True)



model_path = './converted.h5'
classifier_path = "C:/Users/Godwin/Documents/Workflow/opencv/chapter3/\
                    3923_04/cameo/cascades/haarcascade_frontalface_alt.xml"

frmodel, classifier = model(model_path, classifier_path)
woker_cls = register.worker(new_connection,cursor,frmodel, classifier)

woker_cls.register_worker()
woker_cls.sign_out()