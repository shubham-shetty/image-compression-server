#config

import os
import urllib.request
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename

import boto3
s3 = boto3.client('s3')
BUCKET_NAME='sss-compressr'

UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "abc123"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# main.py

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template("index3.html")

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        msg = 'No file part'
        #return redirect(url_for(request.url))
    file = request.files['file']
    if file.filename == '':
        msg = 'No image selected for uploading'
        #return redirect(url_for(request.url))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        msg = 'Image successfully uploaded and displayed below'
        return render_template('index3.html', filename=filename)
    else:
        if not file:
            msg = 'No image selected for uploading'
        else:
            msg = 'Allowed image types are -> png, jpg, jpeg'
        #return redirect(url_for(request.url))
    return render_template("index2.html",msg =msg)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
