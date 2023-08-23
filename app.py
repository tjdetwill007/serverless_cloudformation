import requests
from flask import Flask, render_template,request
import boto3
import json


app = Flask(__name__)

s3 = boto3.client('s3', region_name="us-east-1") #REGION_NAME
@app.route('/')
def hello():
    return render_template("index.html")
    # return 'Hello, World!'
@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return "No photo uploaded", 400

    photo = request.files['photo']
    if photo.filename == '':
        return "No selected photo", 400
    
    ## Generate Pre-signed URL
    presigned_url = s3.generate_presigned_url(
    ClientMethod='put_object',
    Params={
        'Bucket': "mytestlambdaapi", #BUCKET_NAME
        'Key': photo.filename,
    },
    ExpiresIn=3600)
    print(presigned_url)
   

    ##Upload object using pre-signed url's
    response = requests.put(presigned_url, data=photo.filename)

    ## Below is previous method for uploading using aws keys.
    # s3.upload_fileobj(photo, S3_BUCKET, photo.filename) 

    return render_template("uploaded.html")
@app.route('/getdetails', methods=['GET'])
def getdetails():
    data = requests.get("https://02ftwazuji.execute-api.us-west-2.amazonaws.com/Test/") #API LINK
    print(data)
    maindata = data.json()
    print(maindata)
    maindata=json.loads(maindata)
    return render_template("final.html", result=maindata)




app.run(port=80)