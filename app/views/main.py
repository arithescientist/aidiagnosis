from flask import render_template, jsonify, Flask, redirect, url_for, request, flash
from app import app
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
from gevent.pywsgi import WSGIServer
from keras.models import load_model
from flask_cors import CORS, cross_origin




@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
 
@app.route('/upload.html')
def upload():
   return render_template('demo.html')

@app.route('/uploadcnp.html')
def upload_chest():
    return render_template('upload_covid.html')

@app.route('/uploadcnd.html')
def upload_covid():
    return render_template('upload_covid.html')

@app.route('/uploadpnd.html')
def upload_pneumonia():
    return render_template('upload_covid.html')

modelcp = load_model('./app/views/models/modelcnp.h5')
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload_chest.jpg'))

    # resnet_chest = load_model('')
    
    image = cv2.imread('./app/views/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(64,64))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = modelcp.predict(image)
    probability = pred[0]
    print("Model Predictions:")
    color = ""
    status = ""
    message= ""
    result = ""
    if probability[0] > 0.5:
        pred = str('%.2f' % ((probability[0])*100) + '% COVID') 
        color = "danger"
        status = "COVID-19"
        message="The Model found it "
        result = "COVID-19 Positive "
    else:
        pred = str('%.2f' % ((1-probability[0])*100) + '% Pneumonia')
        color = "warning"
        status = "Pneumonia"
        message="The Model found it "
        result = "Pneumonia Positive "
    print(pred)

    return render_template('results.html',predictions=pred, color=color, status=status, message=message, result=result)

modelc = load_model('./app/views/models/modelcnd.h5')
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload_chest.jpg'))

   # resnet_chest = load_model('')
    
    image = cv2.imread('./app/views/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(64,64))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = modelc.predict(image)
    probability = pred[0]
    print("Model Predictions:")
    color = ""
    status = ""
    message= ""
    result = ""
    if probability[0] > 0.5:
        pred = str('%.2f' % ((probability[0])*100) + '% COVID') 
        color = "danger"
        status = "COVID-19"
        message="The Model found it "
        result = "COVID-19 Positive "
    else:
        pred = str('%.2f' % ((1-probability[0])*100) + '% Non-COVID')
        color = "success"
        status = "Normal"
        message="The Model found it "
        result = "Normal "
    print(pred)

    return render_template('results.html',predictions=pred, color=color, status=status, message=message, result=result)

modelp = load_model('./app/views/models/modelpnd.h5')
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'upload_chest.jpg'))

   # resnet_chest = load_model('')
    

    image = cv2.imread( './app/views/uploads/upload_chest.jpg') # read file 
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # arrange format as per keras
    image = cv2.resize(image,(64,64))
    image = np.array(image) / 255
    image = np.expand_dims(image, axis=0)

    pred = modelp.predict(image)
    probability = pred[0]
    print("Model Predictions:")
    color = ""
    status = ""
    message= ""
    result = ""
    if probability[0] < 0.5:
        pred = str('%.2f' % ((1-probability[0])*100) + '% PNEUMONIA') 
        color = "danger"
        status = "Pneumonia"
        message="The Model found it "
        result = "Pneumonia Positive "
    else:
        pred = str('%.2f' % ((probability[0])*100) + '% NON-PNEUMONIA')
        color = "success"
        status = "Normal"
        message="The Model found it "
        result = "Normal "
    print(pred)

    return render_template('results.html',predictions=pred, color=color, status=status, message=message, result=result)


@app.route('/demo')
def demo():
    return render_template('demo.html', title='Demo')
# @app.route('/index')
# def index():
#     return render_template('index.html', title='Home')

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})



@app.route('/contact', methods=['POST'])
def contact():
    first_name = request.form.get("first_name")
    email = request.form.get("email")
    number = int(request.form.get("phone"))
    quest = request.form.get("subject")
    import os

    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASS')

    SUBJECT = "Hello!"
    TEXT = "Thank you! A representative from iDiagnosis will be in touch with you within 24 hours."
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(db_user, db_password)
    server.sendmail(db_user, email, message)


    return render_template('index.html', form=TEXT)


