
from flask import Flask
import pyrebase

config = {
    "apiKey": "AIzaSyDoDIHRceh81ayfHR0PqeNc31h4y0GTdaY",
    "authDomain": "ie-project-292614.firebaseapp.com",
    "databaseURL": "https://ie-project-292614.firebaseio.com",
    "projectId": "ie-project-292614",
    "storageBucket": "ie-project-292614.appspot.com",
    "messagingSenderId": "778120080988",
    "appId": "1:778120080988:web:3f9f009aeb7bcfd6dc4099",
    "measurementId": "G-9VKR4NLKTL"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

db.child("강남대로1").update({"강남대로2": "3.14"})

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
