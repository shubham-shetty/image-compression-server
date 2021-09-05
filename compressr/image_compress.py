import os
import urllib.request
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from compressr.auth import login_required
from compressr.db import get_db

bp = Blueprint('image_compress', __name__)

UPLOAD_FOLDER = 'compressr/static/uploads/'

@bp.route('/home')
def compress_form():
    return render_template("image_compress/index.html")
