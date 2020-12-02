from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('ongkey.json')
defaul_app = firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://ie-project-292614.firebaseio.com/'
})
ref = db.reference('/road')

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
