import pyrebase

config = {
  "apiKey": None,
  "authDomain": None,
  "databaseURL": "https://amongus-htn-default-rtdb.firebaseio.com/",
  "storageBucket": None,
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
db.child("users").child("Morty").update({"test": "lol"})

print(db.child("users").child("Morty").get().val()['test'])