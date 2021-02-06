from flask import Flask, request, jsonify
import json
import boto3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/save', methods=['POST'])
def save_split(receipt, userList):
    """Save an instance of the site with the data pre-loaded from a receipt"""
    content = request.json
    print (content['mytext'])
    return jsonify("content")



def save_receipt(photo):
    bucket = 'bucket'
    detect_text(bucket, photo)
    pass


def detect_text(bucket, photo) -> int:
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
