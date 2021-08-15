from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

app     = Flask(__name__)
app.config.from_object("config")

@app.route("/")
def index():
    return render_template("index.html")

import helpers

@app.route("/", methods=["POST"])
def upload_file():

	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["user_file"]

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
