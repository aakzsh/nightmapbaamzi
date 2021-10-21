from flask import Flask, render_template, request
import numpy as np
from PIL import Image
import base64
import re
from io import BytesIO, StringIO
import cv2

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods = ['GET'])
def index():        
    return render_template('index.html', lat = 30, lng = 70)

@app.route('/image', methods = ['POST'])
def image():
    print("here")
    image_b64 = request.values['imageBase64']
    
    image_PIL = Image.open(BytesIO(base64.b64decode(image_b64.split(",")[1])))
    image_PIL.save('output/10.png')

    return ''


@app.route('/get_image', methods = ['GET'])
def get_image():
    

    return ''
   
if __name__ == "__main__":
    app.run(debug=True)