from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

APP_NAME = 'image-compression-server'
app = Flask(APP_NAME)

@app.route('/')
def upload_page():
    return "Hello World"

@app.route('/form')
def form():
    return render_template('file_submit.html')

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return "File saved successfully"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
