from pymongo import MongoClient
from flask import Flask, request, redirect
import os
from PIL import Image
import json
import boto3

app = Flask(__name__)

HOST = 'localhost'
PORT = 27017
DB_NAME = 'myimagedb'

@app.route('/')
def index():
    client = MongoClient(HOST, PORT)
    db = client[DB_NAME]
    if "metadata" not in db.list_collection_names():
        db.create_collection("metadata")

if __name__ == '__main__':
    app.run(debug=True)

#new upload function
def upload():
    # print('upload')
    file = request.files['form_file'] 
    file.save(os.path.join("./files", file.filename))
    
    #get metadata of the file
    with Image.open(os.path.join("./files", file.filename)) as img:
        size = img.size
        format = img.format
        height = img.height
        width = img.width
        mode = img.mode
        dpi = img.info.get('dpi')
        exif = img.info.get('exif')
        location = os.path.join("./files", file.filename)

    #write to db
    client = MongoClient(HOST, PORT)
    db = client[DB_NAME]
    metadata = {
        "filename": filename,
        "size": size,
        "format": format,
        "width" : width,
        "height": height,
        "mode": mode,
        "dpi": dpi,
        "exif": exif,
        "location": location
    }
    db.metadata.insert_one(metadata)

    #upload to s3
    s3_client = boto3.client('s3', aws_access_key_id='AKIAWZATVY7MB4BXAOIG', aws_secret_access_key= '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')
    s3_client.upload_file(os.path.join("./files", file.filename), "chefomardee-testing", file.filename)

    return redirect("/")
