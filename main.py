
from flask import Flask, render_template, request
import json, wave, base64
from cloud import sendData, retrieveData
from model import model, extract_feature

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        #generate unique file names
        #return result of model
        #potentially ask user whether they are comfortable with storing input/using it to train model
        #if yes, then store input on google cloud and train model with. Else, just run through modela nd return result
        audio = request.files['audio_data']
        audio.save('audio.wav')
        #sendData('audio.wav')
        data = [extract_feature('audio.wav')]
        pred = model.predict(data)
        print(pred)
        
    else:
        return render_template('sound.html')

@app.route('/animal')
def animal():
    return render_template('animal.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)