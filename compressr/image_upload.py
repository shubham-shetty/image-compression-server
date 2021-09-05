import os
import urllib.request
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from compressr.auth import login_required
from compressr.db import get_db

bp = Blueprint('image_upload', __name__)

UPLOAD_FOLDER = 'compressr/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/home')
def upload_form():
    return render_template("image_upload/index.html")

@bp.route('/upload', methods=['POST'])
def image_upload():
    if 'file' not in request.files:
        msg = 'No file part'
        #return redirect(url_for(request.url))
    file = request.files['file']
    if file.filename == '':
        msg = 'No image selected for uploading'
        #return redirect(url_for(request.url))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getcwd(),UPLOAD_FOLDER, filename))
        #print('upload_image filename: ' + filename)
        msg = 'Image successfully uploaded and displayed below'
        return render_template('image_compress/index.html', filename=filename)
    else:
        if not file:
            msg = 'No image selected for uploading'
        else:
            msg = 'Allowed image types are -> png, jpg, jpeg'
        #return redirect(url_for(request.url))
    return render_template("image_upload/index.html",msg =msg)

@bp.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
