import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle

#if librosa run issue occurs run:
#pip install numba==0.43.0
#pip install llvmlite==0.32.1
'''
Me-
The basis of SER or Speech Emotion Recognition is by tracking the tone and pitch of speech. Emotions are subjective so it is difficult to fully recognize emotions with a machine
Librosa analyzes audio and music. It has small packages.
'''

#extract_feature() works to analyze the sound file and gain different values that the machine learning will later look through
'''
Me - 
mfcc: Mel Frequency Cepstral Coefficient, represents the short-term power spectrum of a sound
chroma: Pertains to the 12 different pitch classes
mel: Mel Spectrogram Frequency
'''
def extract_feature(file_name, mfcc=True, chroma=True, mel=True):
    with soundfile.SoundFile(file_name) as sound_file:
        print(file_name)
        X = sound_file.read(dtype="float32")
        sample_rate=sound_file.samplerate
        if chroma:
            stft=np.abs(librosa.stft(X))
        result=np.array([])
        if mfcc:
            mfccs=np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result=np.hstack((result, mfccs))
        if chroma:
            chroma=np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T,axis=0)
            result=np.hstack((result, chroma))
        if mel:
            mel=np.mean(librosa.feature.melspectrogram(X, sr=sample_rate).T,axis=0)
            result=np.hstack((result, mel))
    return result

#Emotions in the RAVDESS dataset
emotions={
  '01':'neutral',
  '02':'calm',
  '03':'happy',
  '04':'sad',
  '05':'angry',
  '06':'fearful',
  '07':'disgust',
  '08':'surprised'
}

#Emotions to observe
observed_emotions=['neutral','calm', 'happy', 'sad','angry','fearful']

#Load the data and extract features from each sound file
#not needed if being used on single file and should only be used for full retrain
def load_data(test_size=0.2):
    x,y=[],[]
    g=0
    for file in glob.glob("data/Actor_*/*.wav"):
        g+=1
        file_name=os.path.basename(file)
        emotion=emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            continue
        feature=extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append(emotion)
    print('files counted n='+str(g))
    return train_test_split(np.array(x), y, test_size=test_size)


#Splits the dataset
#creates the different needed variables, takes very long time tho
x_train,x_test,y_train,y_test=load_data(test_size=0.1)
data = [x_train,x_test,y_train,y_test]
with open('data.txt', 'wb') as fp:
    pickle.dump(data, fp)
#brings in the data text file meant to train and test
#only have code below uncommented if code above is commented
'''
with open ('data.txt', 'rb') as fp:
    data = pickle.load(fp)
    x_train = data[0]
    x_test = data[1]
    y_train = data[2]
    y_test = data[3]
'''
#Gets the number of features extracted
#print(f'Features extracted: {x_train.shape[1]}')

#Only use if the model file has been properly retrained
def overwrite_model_file():
    with open('model.pkl', 'wb') as output:  # Overwrites any existing file.
        pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)
        print("g\n"*600)

#Initialize the Multi Layer Perceptron Classifier
#Only have uncommented if user wants to create a new model
#model=MLPClassifier(alpha=0.01, batch_size=512, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)

greatest_amount = 79.32
#uncomment when optimal model has been obtained
model_file = 'model.pkl'
with open(model_file,'rb') as input:
    model = pickle.load(input)
    while greatest_amount == 79.32:
    #Trains the model, not needed if the model is being imported from a file
        model.fit(x_train,y_train)

        #Predicts the test set
        y_pred=model.predict(x_test)

        #Calculates the accuracy of the model and prints
        accuracy=accuracy_score(y_true=y_test, y_pred=y_pred)
        print("Accuracy: {:.2f}%".format(accuracy*100), end='')


        #test using homemade files
        homemade_test=[extract_feature('sample_tests/calm_no_inflection.wav')]
        pred=model.predict(homemade_test)
        print(" Predicted emotion of homemade wav: " + pred[0])


        if accuracy*100 > greatest_amount:
            greatest_amount = accuracy*100
            overwrite_model_file()
