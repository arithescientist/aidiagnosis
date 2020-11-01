from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app
import random
import os
import cv2
from tensorflow.keras.preprocessing.image import load_img
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input, decode_predictions
import numpy as np

from tensorflow.keras.models import load_model


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/upload.html')
def upload():
   return render_template('upload.html')

@app.route('/upload_chest.html')
def upload_chest():
   return render_template('upload_chest.html')

@app.route('/uploaded_chest', methods = ['GET', 'POST'])
def uploaded_chest():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload_chest.jpg'))
    model = VGG16(weights='imagenet',  include_top = False)
                      
    image = cv2.imread('./app/forms/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(224,224))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)
    x = preprocess_input(image)
                      
    preds = model.predict(x)
    preds_decoded = decode_predictions(preds, top=3)[0]
                      
    print(preds_decoded)
    f.save(path)
                      
    if preds_decoded[0] > 0.5:
        predss = str('%.2f' % (preds_decoded[0]*100) + '% Pneumonia') 
    else:
        predss = str('%.2f' % ((1-preds_decoded[0])*100) + '% Normal')
    print(predss)
    return render_template('results_chest.html', title='Success', predictions=preds_decoded)





@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.seed(41.873937, 41.868075), random.seed(-87.646826, -87.626410))
              for _ in range(random.seed(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@app.route('/demo')
def demo():
    return render_template('demo.html', title='Demo')

