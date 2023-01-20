import dlib, cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

==================================================================
def find_faces(img):
    dets = detector(img, 1)

    if len(dets) == 0:
        return np.empty(0), np.empty(0), np.empty(0)
    
    rects, shapes = [], []
    shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
    for k, d in enumerate(dets):
        rect = ((d.left(), d.top()), (d.right(), d.bottom()))
        rects.append(rect)

        shape = sp(img, d)
        
        # convert dlib shape to numpy array
        for i in range(0, 68):
            shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

        shapes.append(shape)
        
    return rects, shapes, shapes_np

def encode_faces(img, shapes):
    face_descriptors = []
    for shape in shapes:
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        face_descriptors.append(np.array(face_descriptor))

    return np.array(face_descriptors)

======================================================================

img_paths = {
    'NEO':'neo.jpg',
    'KAMIL':'KAMIL.png',
    'MIC':'mic.png',
    'BILL':'BILL.png',
    'LCH':'LCH.jpg',

}

descs = {
    'NEO' :None,
    'KAMIL': None,
    'MIC': None,
    'BILL': None,
    'LCH': None,

}

for name, img_path in img_paths.items():
    img_bgr = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    _, img_shapes, _ = find_faces(img_rgb)
    descs[name] = encode_faces(img_rgb, img_shapes)[0]

np.save('descs.npy', descs)
print(descs)
=======================================================================


import requests
import json

key = '16644288bdc7dd5cfd87e679e9bc291a'
send_url = 'http://api.ipstack.com/check?access_key=' + key
r = requests.get(send_url)
j = json.loads(r.text)

# 경도
lon = str(j['longitude'])

# 위도
lat = str(j['latitude'])

=======================================================================

from pop import LiDAR, Pilot

lidar = LiDAR.Rplidar()
bot = Pilot.SerBot()

import librosa
import cv2
import time
import socket
from pop import Util
import threading
import pymysql

lidar.connect()
lidar.startMotor()
bot.setSpeed(20)
Util.enable_imshow()
fig, ax = plt.subplots(1, figsize=(10, 10))
cam = Util.gstrmer(width=800, height=800)

try:
    camera = cv2.VideoCapture(cam)
    if not camera.isOpened():
        print("Not found camera")
except:
    camera = cv2.VideoCapture(cam)
    if not camera.isOpened():
        print("Not found camera")
        
def LiD():

    while True:
        no_collision = True
        vectors = lidar.getVectors()
        for v in vectors:
            degree = v[0]
            distance = v[1]

            if degree <= 60 or degree >= 200:
                if distance <= 300: 
                    no_collision = False

        if no_collision:
            bot.setSpeed(20)
            bot.forward()
        else:
            bot.setSpeed(20)
            bot.turnLeft()
        
        
def face():
    while(True):
        global name
        fig, ax = plt.subplots(1, figsize=(10, 10))
        ret, img_bgr = camera.read()
        img_rgb= cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        rects, shapes, _ = find_faces(img_rgb)
        descriptors = encode_faces(img_rgb, shapes)
        ax.imshow(img_rgb)
        for i, desc in enumerate(descriptors):

            found = False
            for name, saved_desc in descs.items():
                dist = np.linalg.norm([desc] - saved_desc, axis=1)

                if dist < 0.6:
                    found = True

                    text = ax.text(rects[i][0][0], rects[i][0][1], name,
                            color='b', fontsize=40, fontweight='bold')
                    text.set_path_effects([path_effects.Stroke(linewidth=10, foreground='white'), path_effects.Normal()])
                    rect = patches.Rectangle(rects[i][0],
                                            rects[i][1][1] - rects[i][0][1],
                                            rects[i][1][0] - rects[i][0][0],
                                            linewidth=2, edgecolor='w', facecolor='none')
                    ax.add_patch(rect)
                    print(name)
                    break

            if not found:
                ax.text(rects[i][0][0], rects[i][0][1], 'unknown',
                        color='r', fontsize=20, fontweight='bold')
                rect = patches.Rectangle(rects[i][0],
                                        rects[i][1][1] - rects[i][0][1],
                                        rects[i][1][0] - rects[i][0][0],
                                        linewidth=2, edgecolor='r', facecolor='none')
                ax.add_patch(rect)  
                print("unknown")
        plt.axis('off')
        plt.show()
        plt.close()
        plt.cla()
        plt.clf()
        print(name)
        print(lat,lon)
        time.sleep(4)
        
def server():
    global sql
    conn = pymysql.connect(host="192.168.0.12", user="root",
                       password="1234", db="PoliceBot", charset="utf8")
    cur = conn.cursor()
    if name == 'LST':
        sql = "select * from person WHERE personNum = '2'"
    elif name == 'LCH':
        sql = "select * from person WHERE personNum = '1'"
        
    
        
    cur.execute(sql)
    row = cur.fetchone()

    if row == None:
        print('검색결과없음')
    else:
        print("id = ", row[0],"\n",
              "name = ", row[1],"\n",
              "birth = ", row[2],"\n",
              "missing or wanted = ", row[3],"\n")
    conn.close()
    
    host = '192.168.0.15'  # 호스트 ip를 적어주세요 
    port = 9998      # 포트번호를 임의로 설정해주세요 

    server_sock = socket.socket(socket.AF_INET) 
    server_sock.bind((host, port)) 
    server_sock.listen(1)
    
    print("기다리는 중") 
    client_sock, addr = server_sock.accept() 

    personName = row[1]
    personBirth = row[2]
    personFeature = row[3]


    client_sock.sendall(personName.encode("utf-8"))
    client_sock.sendall(personBirth.encode("utf-8"))
    client_sock.sendall(personFeature.encode("utf-8"))
    client_sock.sendall(lat.encode("utf-8"))
    client_sock.sendall(lon.encode("utf-8"))

    client_sock.close()
    server_sock.close()
    

threading.Thread(target=LiD).start()
threading.Thread(target=face).start()
threading.Thread(target=server).start()











