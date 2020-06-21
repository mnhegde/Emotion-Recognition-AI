import librosa
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle

def extract_feature(file_name, mfcc=True, chroma=True, mel=True):
    with soundfile.SoundFile(file_name) as sound_file:
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

def open_model():
    with open('model.pkl', 'rb') as input:
        model = pickle.load(input)
        return(model)

def overwrite_model_file(model):
    with open('model.pkl', 'wb') as output:
        pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)
        print('succesfully trained')

def model_predict(file_name):
    extracted_features = [extract_feature(file_name)]

    model = open_model()
    
    pred = model.predict(extracted_features)
    
    return(pred)


def model_train(file_name, emotion):
    extracted_features = [extract_feature(file_name)]

    correct_emotion = [emotion]

    model = open_model()
    
    model.fit(extracted_features,correct_emotion)

    overwrite_model_file(model)

print(model_predict('sample_tests/')[0])