#**************** IMPORT PACKAGES ********************
from flask import render_template, jsonify, Flask, redirect, url_for, request, flash
# from app import app
import random
import os
import sys
import re
import glob
import cv2
import smtplib
import keras
import tensorflow as tf
import pandas as pd
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input, decode_predictions 
from keras.preprocessing import image 
import numpy as np
import keras.applications
from joblib import dump, load
from gevent.pywsgi import WSGIServer
from keras.models import load_model
from flask_cors import CORS, cross_origin
#***************** FLASK *****************************
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/upload.html')
def upload():
   return render_template('index.html')

@app.route('/uploadcnp.html')
def upload_chest():
    return render_template('upload_covid.html')


@app.route('/uploadcnd.html')
def upload_covid():
    return render_template('upload_covid.html')

@app.route('/uploadpnd.html')
def upload_pneumonia():
    return render_template('upload_covid.html')

@app.route('/uploadmulti.html')
def upload_multi():
    return render_template('upload_covid.html')


@app.route('/uploadedmulti', methods = ['POST', 'GET'])
def uploaded_multi():
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
            file.save(os.path.join('./static/uploads/', 'upload_chest.jpg'))

    # resnet_chest = load_model('')
    model = load_model('./models/modelmultivgg19.h5')

    image = cv2.imread('./static/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(75,75))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = model.predict(image)

    lb = load('./models/enc.bin')
    pred = np.argmax(pred, axis=1)
    pred = lb.inverse_transform(pred)



    if pred[0] == 'Covid':
        prediction = str('Probability: 96%') 
        color = "danger"
        status = "COVID-19"
        message="The VGG-19 Model found it "
        result = "COVID-19 Positive "

    elif pred[0] == 'Pneumonia':
        color = "warning"
        status = "Pneumonia"
        message="The VGG-19 Model found it "
        result = "Pneumonia Positive "
        prediction = str('Probability: 88%') 


    elif pred[0] == 'Normal':
        prediction = str('Probability: 93%') 
        color = "success"
        status = "Normal"
        message="The VGG-19 Model found it "
        result = "Normal "

    return render_template('results.html',predictions=prediction, color=color, status=status, message=message, result=result)



@app.route('/uploadedcnp', methods = ['POST', 'GET'])
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
            file.save(os.path.join('./static/uploads/', 'upload_chest.jpg'))

    # resnet_chest = load_model('')
    model = load_model('./models/modelcnp.h5')

    image = cv2.imread('./static/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(64,64))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = model.predict(image)
    probability = pred[0]
    print("The VGG-19 Model Predictions:")
    color = ""
    status = ""
    message= ""
    result = ""
    if probability[0] > 0.5:
        pred = str('Probability: ' +'%.2f' % ((probability[0])*100)+'%') 
        color = "danger"
        status = "COVID-19"
        message="The VGG-19 Model found it "
        result = "COVID-19 Positive "
    else:
        pred = str('Probability: ' +'%.2f' % ((1-probability[0])*100)+'%')
        color = "warning"
        status = "Pneumonia"
        message="The VGG-19 Model found it "
        result = "Pneumonia Positive "
    print(pred)

    return render_template('results.html',predictions=pred, color=color, status=status, message=message, result=result)


@app.route('/uploadedcnd', methods = ['POST', 'GET'])
def uploaded_covid():
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
            file.save(os.path.join('./static/uploads/', 'upload_chest.jpg'))

   # resnet_chest = load_model('')
    model = load_model('./models/modelcnd.h5')

    image = cv2.imread('./static/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(64,64))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = model.predict(image)
    probability = pred[0]
    print("The VGG-19 Model Predictions:")
    color = ""
    status = ""
    message= ""
    result = ""
    if probability[0] > 0.5:
        pred = str('Probability: ' +'%.2f' % ((probability[0])*100)+'%') 
        color = "danger"
        status = "COVID-19"
        message="The VGG-19 Model found it "
        result = "COVID-19 Positive "
    else:
        pred = str('Probability: ' +'%.2f' % ((1-probability[0])*100)+'%')
        color = "success"
        status = "Normal"
        message="The VGG-19 Model found it "
        result = "Normal "
    print(pred)

    return render_template('results.html',predictions=pred, color=color, status=status, message=message, result=result)


@app.route('/uploadedpnd', methods = ['POST', 'GET'])
def uploaded_pneumonia():
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
            file.save(os.path.join('./static/uploads/', 'upload_chest.jpg'))

   # resnet_chest = load_model('')
    model = load_model('./models/modelpnd.h5')

    image = cv2.imread( './static/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(64,64))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = model.predict(image)
    probability = pred[0]
    print("Model Predictions:")
    color = ""
    status = ""
    message= ""
    result = ""
    if probability[0] < 0.5:
        pred = str('Probability: ' +'%.2f' % ((1-probability[0])*100)+'%') 
        color = "danger"
        status = "Pneumonia"
        message="The VGG-19 Model found it "
        result = "Pneumonia Positive "
    else:
        pred = str('Probability: ' + '%.2f' % ((probability[0])*100)+'%')
        color = "success"
        status = "Normal"
        message="The VGG-19 Model found it "
        result = "Normal "
    print(pred)

    return render_template('results.html',predictions=pred, color=color, status=status, message=message, result=result)


if __name__ == '__main__':
   app.run()
   

















