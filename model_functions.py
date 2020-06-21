import librosa
from librosa.core import istft
import soundfile
import os, glob, pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import pickle

def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        X = librosa.to_mono(X)
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
    #do not mess with
    with open('model.pkl', 'wb') as output:
        pickle.dump(model, output, pickle.HIGHEST_PROTOCOL)
        print('succesfully trained')

def save_batch_data(data,emotion):
    with open ('batch_data_x.txt', 'rb') as fp:
        batch_data_x = pickle.load(fp)

    batch_data_x.append(data)

    with open ('batch_data_y.txt', 'rb') as fp:
        batch_data_y = pickle.load(fp)

    batch_data_y.append(emotion)

    with open('batch_data_x.txt', 'wb') as fp:
        pickle.dump(batch_data_x, fp)
    
    with open('batch_data_y.txt', 'wb') as fp:
        pickle.dump(batch_data_y, fp)

def reset_batch_data():
    batch_data_x = []
    batch_data_y = []

    with open('batch_data_x.txt', 'wb') as fp:
        pickle.dump(batch_data_x, fp)
    
    with open('batch_data_y.txt', 'wb') as fp:
        pickle.dump(batch_data_y, fp)

def open_batch_data(xy):
    if xy == 'x':
        with open ('batch_data_x.txt', 'rb') as fp:
            batch_data_x = pickle.load(fp)
            return(batch_data_x)
    if xy == 'y':
        with open ('batch_data_y.txt', 'rb') as fp:
            batch_data_y = pickle.load(fp)
            return(batch_data_y)

def model_predict(file_name):
    extracted_features = [extract_feature(file_name, mfcc=True, chroma=True, mel=True)]
    model = open_model()
    
    model.batch_size = 256
    pred = model.predict(extracted_features)
    
    return(pred)


def model_train(file_name, emotion):
    
    extracted_features = extract_feature(file_name, mfcc=True, chroma=True, mel=True)
    save_batch_data(extracted_features, emotion)

    batch_data_y = open_batch_data('y')
    batch_data_x = open_batch_data('x')

    if len(batch_data_y) == 2017:
        model = open_model()
        model.fit(batch_data_x,batch_data_y)
        overwrite_model_file(model)


chosen_file = "sample_tests/calm_no_inflection.wav"
emotion = 'angry'
print(model_predict(chosen_file)[0])
#model_train(chosen_file, emotion)