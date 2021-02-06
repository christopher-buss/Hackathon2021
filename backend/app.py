import logging
import os

import boto3
from botocore.exceptions import ClientError
from flask import Flask, request, jsonify, flash, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/save', methods=['POST'])
def save_split(receipt, userList):
    """Save an instance of the site with the data pre-loaded from a receipt"""
    content = request.json
    print(content['mytext'])
    return jsonify("content")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/save_receipt', methods=['POST'])
def upload_file():
    """https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/"""
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'photo' not in request.files:
            print('No photo')
            return redirect(request.url)
        file = request.files['photo']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected photo')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            print("Uploaded file")
            return 'Success'
    return redirect(request.url)


def save_receipt():
    pass


def detect_text(bucket, photo) -> int:
    """https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html"""
    client = boto3.client('rekognition')
    response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    text_detections = response['TextDetections']
    print('Detected text\n----------')
    for text in text_detections:
        print('Detected text:' + text['DetectedText'])
        print('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
        print('Id: {}'.format(text['Id']))
        if 'ParentId' in text:
            print('Parent Id: {}'.format(text['ParentId']))
        print('Type:' + text['Type'])
        print()
    return len(text_detections)


if __name__ == '__main__':
    app.run()
