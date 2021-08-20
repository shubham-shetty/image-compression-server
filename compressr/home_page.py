from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from compressr.auth import login_required
from compressr.db import get_db

bp = Blueprint('home_page', __name__)

@bp.route('/')
def index():
    db = get_db()
    return render_template('home_page/index.html')
