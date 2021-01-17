import pyrebase

url = "https://amongus-htn-default-rtdb.firebaseio.com/"

class FirebaseHandler:
    def __init__(self):
        config = {
            "apiKey": None,
            "authDomain": None,
            "databaseURL": url,
            "storageBucket": None,
        }

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()