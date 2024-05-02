from flask import Flask 
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return "Homepage"

@app.route('/rep')
def getServers():
    return


if __name__ == '__main__':
    app.run(debug=True)
