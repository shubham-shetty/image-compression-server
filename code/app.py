from flask import Flask, jsonify, request

APP_NAME = 'image-compression-server'
app = Flask(APP_NAME)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')