import logging
import os

import boto3
from database_interaction import add_receipt, retrieve_receipt
from botocore.exceptions import ClientError
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS, cross_origin

from connection import ItemJSONEncoder

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.json_encoder = ItemJSONEncoder

CORS(app)


@app.route('/save', methods=['POST'])
@cross_origin()
def save_instance():
    """Save an instance of the site with the data pre-loaded from a receipt"""
    receipt = request.json["receipt"]
    splits = request.json["splits"]
    receipt_id = add_receipt(receipt["name"], receipt["items"], receipt["total"], splits)
    return str(receipt_id)


@app.route('/return/<receipt_id>', methods=['GET'])
@cross_origin()
def return_instance(receipt_id):
    """Return to a saved instance of the site from the database"""
    receipt = retrieve_receipt(receipt_id=receipt_id)
    print(type(receipt))
    return jsonify(receipt)


def allowed_file(filename):
    """Check if the file is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/save_receipt', methods=['GET', 'POST'])
@cross_origin()
def client_upload_file():
    """https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/"""
    if request.method == 'POST':
        # check if the post request has the file part
        print(request.files)
        if 'photo' not in request.files:
            print('No photo')
            return "FAILED", 400
        file = request.files['photo']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            print('No selected photo')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            save_receipt_to_amazon_s3(UPLOAD_FOLDER + '/' + file.filename, file.filename)
            detect_text(file.filename)
            print("Uploaded file")
            return 'Success'
    return "Failed", 400


def save_receipt_to_amazon_s3(path, file_name):
    """Saves the receipt to amazon s3 bucket"""
    print("Uploading image...")
    s3 = boto3.client('s3')
    try:
        s3.upload_file(path, "hackaway-v4", file_name,
                       ExtraArgs={'ContentType': 'image/png'})
    except ClientError as e:
        logging.error(e)
        print("---__---")
        return False
    print("Remove file:", path)
    os.remove(path)
    return True


def detect_text(photo) -> int:
    """https://docs.aws.amazon.com/rekognition/latest/dg/text-detecting-text-procedure.html"""
    client = boto3.client('rekognition', region_name='eu-west-2')
    response = client.detect_text(Image={'S3Object': {'Bucket': 'hackaway-v4', 'Name': photo}},
                                  Filters={'WordFilter': {'MinConfidence': 0.9}})

    text_detections = response['TextDetections']
    print([det['DetectedText'] for det in text_detections])  # if det['Confidence'] > 90])
    return len(text_detections)


if __name__ == '__main__':
    app.run()
