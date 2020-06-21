
from flask import Flask, render_template, request
import json, wave, base64
from cloud import sendData, retrieveData

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        audio = request.files['audio_data']
        audio.save('audio.wav')
        sendData('audio.wav')
    else:
        return render_template('sound.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)