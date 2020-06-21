
from flask import Flask, render_template, request
import json
import base64

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Open file and write binary (blob) data
        f = open('./file.wav', 'wb')
        encode_string=base64.b64encode(request.json)
        decode_string = base64.b64decode(encode_string)
        f.write(decode_string)
        
     
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)