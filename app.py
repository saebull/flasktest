from flask import Flask, render_template, redirect, request, url_for
import requests
from bs4 import BeautifulSoup
import re

def getlatlng(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/xml?address="
    url = base_url + address + "CA&key=AIzaSyBHLxYz1nqgbaj-SIxnBXtvWiLiXAr1LNQ"
    res = requests.get(url)
    html = BeautifulSoup(res.text,'html.parser')
    lat = re.sub('<[^>]*>', '',str(html.select("location > lat")) ,0)##위도
    lng = re.sub('<.+?>', '',str(html.select("location > lng")) ,0) ##경도
    lat = float(lat.replace('[', '').replace(']', ''))
    lng = float(lng.replace('[', '').replace(']', ''))
    return lat,lng

app = Flask(__name__)


@app.route('/')
def inputTest():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
       dep = request.form['departure']
       des = request.form['destination']
       dep_lat, dep_lng = getlatlng(dep)
       des_lat, des_lng = getlatlng(des)

       return render_template("generic.html", dep_lat=dep_lat, dep_lng=dep_lng, des_lat=des_lat, des_lng=des_lng)

@app.route('/elements')
def elements():
       return render_template('elements.html')

@app.route('/index')
def index():
       return render_template('index.html')

@app.route('/generic')
def generic():
       return render_template('generic.html')


if __name__ == '__main__':
    app.run()
