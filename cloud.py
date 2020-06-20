import logging, os
from flask import Flask, request
from google.cloud import storage

storage_client = storage.Client.from_service_account_json("CloudKey.json")

bucket = storage_client.get_bucket("emotion-recognition-data")

def sendData():

    filename = open('download.png', 'rb')

    blob = bucket.blob('dog.png')

    blob.upload_from_file(filename)

def retrieveData():
    blob = bucket.get_blob('dog.png')
    blob.download_to_filename('dog.png')


retrieveData()