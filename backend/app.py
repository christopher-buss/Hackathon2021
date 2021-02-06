import logging
import os

import boto3
from database_interaction import add_receipt
from botocore.exceptions import ClientError
from flask import Flask, request, redirect

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/save', methods=['POST'])
def save_instance():
    """Save an instance of the site with the data pre-loaded from a receipt"""
    receipt = request.json["receipt"]
    splits = request.json["splits"]
    receipt_id = add_receipt(receipt["name"], splits, receipt["total"])
    return receipt_id


def allowed_file(filename):
    """Check if the file is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/save_receipt', methods=['POST'])
def client_upload_file():
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
            save_receipt_to_amazon_s3(UPLOAD_FOLDER + '/' + file.filename, file.filename)
            detect_text(file.filename)
            print("Uploaded file")
            return 'Success'
    return redirect(request.url)


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
