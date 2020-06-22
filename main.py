
from flask import Flask, render_template, request
import json, wave, base64, glob, model_functions, os
#from cloud import sendData, retrieveData

app = Flask(__name__)

filesAdded = {}
keys = []

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
<<<<<<< HEAD
        if consent == True:
            #sendData(filename)
=======
        if consent == 'true':
            sendData(filename)
>>>>>>> e2f6f0fe67924f3bfc2b0c2095100326801a3b70
            filesAdded[filename] = result[0]
        elif consent == 'false':
            os.remove(filename)
        return result[0] + ' ' + data['Id']
    else:
        return render_template('sound.html')

@app.route('/trainModel', methods=['GET', 'POST'])
def trainModel():
    if request.method == 'POST':
        data = request.json
        for key in filesAdded.keys():
            keys.append(key)
        prediction = keys[0]
        if data['Prediction'] == 'Correct':
            model_functions.model_train(prediction[0], prediction[1])
        if data['Prediction'] == 'Wrong':
            correctEmotion = data['Emotion']
            model_functions.model_train(prediction[0], correctEmotion)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)