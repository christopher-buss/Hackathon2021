from flask import Flask, request, jsonify
import json
import boto3
import connection

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/save', methods=['POST'])
def save_split(receipt, userList):
    """Save an instance of the site with the data pre-loaded from a receipt"""
    connection.connect()
    content = request.json
    print(content['mytext'])
    return jsonify("content")


@app.route('/save_receipt', methods=['POST'])
def save_receipt():
    bucket = 'arn:aws:s3:eu-west-2:082286152231:accesspoint/hackaway'
    print(request.form)
    photo = request.form['photo']
    detect_text(bucket, photo)


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
