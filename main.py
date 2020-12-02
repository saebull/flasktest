import pyrebase
from flask import *

config = {
    apiKey: "AIzaSyDoDIHRceh81ayfHR0PqeNc31h4y0GTdaY",
    authDomain: "ie-project-292614.firebaseapp.com",
    databaseURL: "https://ie-project-292614.firebaseio.com",
    projectId: "ie-project-292614",
    storageBucket: "ie-project-292614.appspot.com",
    messagingSenderId: "778120080988",
    appId: "1:778120080988:web:3f9f009aeb7bcfd6dc4099",
    measurementId: "G-9VKR4NLKTL"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
user = auth.sign_in_with_email_and_password(ny3021@gmail.com, dud30218856)


db = firebase.database()

app = Flask(__name__)

db.child("road").child("강남대로1").update({"강남대로2": "3.14"})


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        name = request.form['name']
        db.child('todo').push(name)
        todo = db.child('todo').get()
        todo_list = todo.val()
        return render_template('index.html', todo=todo_list)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)