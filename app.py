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
def index():        
    return render_template('index.html', lat = 30, lng = 70)

@app.route('/image', methods = ['POST'])
def image():
    print("here")
    image_b64 = request.values['imageBase64']
    
    image_PIL = Image.open(BytesIO(base64.b64decode(image_b64.split(",")[1])))
    img_id = str(uuid.uuid4())
    image_PIL.save(f"{img_id}.png")

    blob = bucket.blob(f"{img_id}.png")
    imgpath = f"E:\\nightmapbaamzi\\{img_id}.png"
    with open(imgpath, 'rb') as my_file:
        blob.upload_from_file(my_file)
    print(blob.public_url)
    return ''


@app.route('/get_image', methods = ['GET'])
def get_image():
    image_id = request.form.get('image_id')

    return ''
   
if __name__ == "__main__":
    app.run(debug=True, threaded = True)