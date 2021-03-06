import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


from flask import Flask, render_template, redirect, request, url_for
import requests
from bs4 import BeautifulSoup
import re
import heapq
import json

with open('finalmap.json', 'r',encoding='utf-8',) as f:
    lst = json.load(f)

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

def getPos(x, y):
    read = pd.read_excel('위도경도데이터_잠원동_raw.xlsx', sheet_name='Sheet1')
    path = pd.DataFrame(read)
    #print(path)
    df1 = pd.concat([path['p1위도'], path['p1경도']],axis=1)
    df2 = pd.concat([path['p2위도'], path['p2경도']], axis =1)
    df = pd.concat([df1,df2],axis=1)
    x = float(x)
    y = float(y)
    position1=[]
    position2 =[]
    for i in range(len(df)):
        if abs(x - df.loc[i,'p1위도']) + abs(y - df.loc[i,'p1경도']) > abs(x - df.loc[i,'p2위도']) + abs(y - df.loc[i,'p2경도']):
            position1.append([i,abs(x - df.loc[i,'p1위도']) + abs(y - df.loc[i,'p1경도'])])
        else:
            position2.append([i,abs(x - df.loc[i,'p2위도']) + abs(y - df.loc[i,'p2경도'])])
    minn = 1000
    result1 =0
    result2 = 0
    if min(position1[1]) > min(position2[1]):
        for j in position1 :
            if minn > j[1]:
                minn = j[1]
                result1 = j[0]
    else:
        for j in position2 :
            if minn > j[1]:
                minn = j[0]
                result2 = j[0]

    if result1 >0:
        road =path.loc[result1,'도로명']
        return road
    else :
        road =path.loc[result2,'도로명']
        return road

def dijkstra(graph, start, end):
    visited = {start: 0}
    h = [(0, start)]
    path = {}
    lst=[]
    distances = {vertex: float('inf') for vertex in graph} # 시작점과 모든 정점과의 사리의 거리를 무한으로 지정
    #istances[start] = [0, start] # 시작점과 시작점 사이의 거리 0
    #queue = [] # [[거리,정점]]
    #print(distances[start][0])
    #heapq.heappush(queue, [distances[start][0], start])
    while distances:
        current_distance, current_vertex = heapq.heappop(h)
        try:
            while current_vertex not in distances:
                current_distance, current_vertex = heapq.heappop(h)
        except IndexError:
             break
        #if distances[current_vertex][0] < current_distance:
            #continue

        if current_vertex == end:
            way = end
            lst.append(way)
            path_output = end + '->'
            while path[way] != start:
                path_output += path[way] + '->'
                way = path[way]
                lst.append(way)
            lst.append(start)
            path_output += start
            print(path_output)

            return visited[end], path, lst

        del distances[current_vertex]

        for v, weihgt in graph[current_vertex].items():
            weihgt = current_distance + weihgt
            #if weihgt < distances[adjacent][0]: # 현재까지 시작정점과 현재정점사이의 거리보다 짧다면
                #distances[adjacent] = [dis, current_vertex] # 현재정점과 시작정점 사이의 거리 업데이트
                #heapq.heappush(queue, [dis, adjacent])

            if v not in visited or weihgt < visited[v] :
                visited[v] = weihgt
                heapq.heappush(h,(weihgt,v))
                path[v] = current_vertex


    return visited,path,lst

def findlatlng(name):
    read = pd.read_excel('위도경도데이터_잠원동_raw.xlsx', usecols=[1,2,3])
    path = pd.DataFrame(read)
    lat = path[path['도로명']==name].iloc[:,1].values
    lng = path[path['도로명']==name].iloc[:,2].values
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
       s = getPos(dep_lat, dep_lng)
       e = getPos(des_lat, des_lng)
       (a, b, c) = dijkstra(lst, s, e)
       temp = []
       for i in c:
           ss,ee = findlatlng(i)
           temp.append((ss[0],ee[0]))
       return render_template("generic.html", dep_lat=dep_lat, dep_lng=dep_lng, des_lat=des_lat, des_lng=des_lng, temp=temp)

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
