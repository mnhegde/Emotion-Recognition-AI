
from flask import Flask, render_template, request
import json, wave, base64, glob, model_functions, os
from cloud import sendData, retrieveData
#from model import model, extract_feature

app = Flask(__name__)

filesAdded = {}

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        audio = request.files['audio_data']
        data = request.form
        consent = data['Consent']
        existingFiles = len(glob.glob('userInput/*'))
        filename = 'userInput/audio%s.wav' %(existingFiles + 1)
        audio.save(filename)
        result = model_functions.model_predict(filename)
        if consent == True:
            sendData(filename)
            filesAdded[filename] = result[0]
        elif consent == False:
            os.remove(filename)
        return result[0] + ' ' + data['Id']
    else:
        return render_template('sound.html')

@app.route('/trainModel', methods=['GET', 'POST'])
def trainModel():
    if request.method == 'POST':
        data = request.json
        prediction = next(iter(filesAdded.items() ))
        if data['Prediction'] == 'Correct':
            model_functions.model_train(prediction[0], prediction[1])
        if data['Prediction'] == 'Wrong':
            correctEmotion = data['Emotion']
            model_functions.model_train(prediction[0], correctEmotion)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)