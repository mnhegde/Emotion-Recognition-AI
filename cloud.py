import logging, os, wave
from google.cloud import storage

storage_client = storage.Client.from_service_account_json("CloudKey.json")
bucket = storage_client.get_bucket("emotion-recognition-data")

def sendData(filename):
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

def retrieveData(filename):
    blob = bucket.get_blob(filename)
    blob.download_to_filename(filename)


