from flask from Flask 
import socket

app = Flask(__name__)

@app.route('/')
def home():
    return "Homepage"

@app.route('/rep')
def getservers():
    return


if __name__ == '__main__':
    app.run(debug=True)
