from flask import render_template, jsonify, Flask, redirect, url_for, request, flash
from app import app
import random
import os
import sys
import re
import glob
#import cv2
import keras
import tensorflow as tf
import pandas as pd
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from keras.applications.inception_v3 import InceptionV3
from keras.applications.imagenet_utils import preprocess_input, decode_predictions 
from keras.preprocessing import image 
import numpy as np
import keras.applications
from gevent.pywsgi import WSGIServer
from keras.models import load_model
from flask_cors import CORS, cross_origin

MODEL_PATH = 'h1.h5'

# Load your trained model
model = load_model(MODEL_PATH)


cors = CORS(app)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)

    preds = model.predict(x.T)
    return preds


@app.route('/')
@app.route('/index')
@cross_origin()
def index():
    return render_template('index.html', title='Home')

@app.route('/demo')
@cross_origin()
def demo():
    return render_template('demo.html', title='Demo')


@app.route('/upload')
@cross_origin()
def upload_file2():
    return render_template('demo.html', title='Home')


@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        df = pd.DataFrame(preds, columns= ['COVID','NORMAL','PNEUMONIA'])

        # Process your result for human
        #pred_class = preds.argmax(axis=-1)            # Simple argmax
        pred_class = decode_predictions(df, top=1)   # ImageNet Decode
        result = str(pred_class[0][0][1])               # Convert to string
        # return result

        # results = ""
        # e = ""

        # if (df['COVID'][0] > 0.5):
        #     e =  df['COVID'][0]
        #     results = 'COVID-19 POSITIVE WITH {:.2%} CERTAINTY'.format(e)
        #     print(results)
        # elif (df['NORMAL'][0] > 0.5):
        #     e =  df['NORMAL'][0]
        #     results = 'COVID & PNEUMONIA NEGATIVE WITH {:.2%} CERTAINTY'.format(e)
        #     print(results)

        # elif (df['PNEUMONIA'][0] > 0.5):
        #     e =  df['PNEUMONIA'][0]
        #     results = 'PNEUMONIA POSITIVE WITH {:.2%} CERTAINTY'.format(e)
        #     print(results)

        # result = df.idxmax(axis=1)[0]
        # t = df.max(axis=1)
        # w = " WITH "
        # result = result + w + "{:.2%} CERTAINTY".format(float(t))
        # result = result + t
        return result
        #return render_template('index.html', predictions=e)
    return None



@app.route('/map')
@cross_origin()
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
@cross_origin()
def map_refresh():
    points = [(random.seed(41.873937, 41.868075), random.seed(-87.646826, -87.626410))
              for _ in range(random.seed(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
@cross_origin()
def contact():
    return render_template('contact.html', title='Contact')



