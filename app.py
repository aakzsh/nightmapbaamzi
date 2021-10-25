from flask import Flask, render_template, request
import numpy as np
from PIL import Image
import base64
import re
from io import BytesIO, StringIO
import cv2

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage
import uuid

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'awestruck-d86c7.appspot.com'
})

app = Flask(__name__)
app.config["DEBUG"] = True

db = firestore.client()


bucket = storage.bucket()

@app.route('/', methods = ['GET'])
def start(): 
    return render_template('index.html')

@app.route('/night', methods = ['GET'])
def index(): 
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    code = request.args.get("code")
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    dt = request.args.get("time")

    if(dt == "now"):
        date = "now"
    else:
        sp_dt = dt.split("-")
        y = int(sp_dt[0])
        m = int(sp_dt[1])
        d = int(sp_dt[2])
        t = sp_dt[3]
        month = months[m-1]

        date = f"{month} {d} {y} {t}"
    # lat = 90
    # lng = 90
    # code = "ll"
    # date = 'June 20 1998'
      
    # print(code,lat,lng)
    return render_template('homee.html', lat = int(lat), lng = int(lng), code=code, date=date)

@app.route('/image', methods = ['POST'])
def image():
    print("here")
    image_b64 = request.values['imageBase64']
    code = request.values['code']
    print(code)
    db.collection('room').document(f'{code}').set({
        u'url': str(image_b64).split(",")[1],
    })
    
    print("success")
    # image_PIL = Image.open(BytesIO(base64.b64decode(image_b64.split(",")[1])))
    # img_id = str(uuid.uuid4())
    # image_PIL.save(f"{img_id}.png")

    # blob = bucket.blob(f"{img_id}.png")
    # imgpath = f"E:\\nightmapbaamzi\\{img_id}.png"
    # with open(imgpath, 'rb') as my_file:
    #     blob.upload_from_file(my_file)
    # print(blob.public_url)

    return ''


@app.route('/get_image', methods = ['GET'])
def get_image():
    image_id = request.form.get('image_id')
    return ''

@app.route('/walk_stats/<name>/<steps_today>/<total_steps>/<level>')
def walk_stats(name,steps_today,total_steps,level):
    return render_template('walk_stats.html', name= name, steps_today=steps_today, total_steps=total_steps,level=level)
   
@app.route('/meditation_stats/<name>/<total_time>')
def meditation_stats(name,total_time):
    return render_template('meditation_stats.html', name= name, total_time=total_time)

if __name__ == "__main__":
    app.run(debug=True, threaded = True)