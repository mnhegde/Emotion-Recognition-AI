from scipy.io.wavfile import write, read
from flask import Flask, render_template, request
import simpleaudio as sa
import json
import io
app = Flask(__name__)

def convertAudio(data):
    print(data)
    rate, data = read(io.BytesIO(data))
    reversed_data = data[::-1]
    bytes_wav = bytes()
    byte_io = io.BytesIO(bytes_wav)
    write(byte_io,rate,reversed)
    output_wav = byte_io.read()

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        convertAudio(request.json)
     
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)