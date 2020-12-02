import pyrebase
from flask import *

config = {
    "apiKey": "AIzaSyAsDlGTnwNoRgAdcoMV41x_xxxxx",
    "authDomain": "pythontest-xxxx.firebaseapp.com",
    "databaseURL": "https://pythontest-xxxx.firebaseio.com",
    "projectId": "pythontest-xxxx",
    "storageBucket": "",
    "messagingSenderId": "68980739xxxx",
    "appId": "1:689807391396:web:cedfcfbb5xxxxx"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

app = Flask(__name__)

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