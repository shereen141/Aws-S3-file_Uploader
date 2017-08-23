from flask import Flask, render_template

app = Flask(__name__)

from flask import Flask, request, render_template, send_from_directory
import boto3
import boto3.s3
import botocore

app = Flask(__name__)

Access_Key_ID=
Secret_Access_Key=


def connectS3():
    return boto3.resource(
        service_name='s3',
        aws_access_key_id=Access_Key_ID,
        aws_secret_access_key=Secret_Access_Key,
        region_name='us-east-2'
       )

@app.route('/upload', methods=['POST','GET'])
def toUpload():
    if request.method == 'POST':
        file = request.files['file']
        numb = request.form.get('numb')
        upload(file,numb)
        return 'uploaded!'
    else:
        return 'failed!'


def upload(file,numb):
    conn = connectS3()
    bucket = conn.Bucket('file-6331')
    fileName = file.filename
    #root = app.root_path
    data = file.read()
    conn.Bucket(bucket.name).put_object(Key=numb+'_'+fileName, Body=data)


@app.route('/download', methods=['POST','GET'])
def toDownload():
    if request.method == 'POST':
        file = request.form.get('file1')
        file = download(file)
        root = app.root_path
        filepath = root + '/static/' + file
        return render_template('view.html',file=file)

    else:
        return 'failed'

def download(file):
    conn = connectS3()
    bucket = conn.Bucket('file-6331')
    root = app.root_path
    filepath = root + '/static/' + file
    try:
        conn.Bucket(bucket.name).download_file(file, filepath)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    return file


    



@app.route('/')
def hello_world():
    conn = connectS3()
    bucket = conn.Bucket('file-6331')
    fileList = []
    for fileObj in bucket.objects.all():
        fileList.append(fileObj.key)
    return render_template('index.html', fileList=fileList)


if __name__ == '__main__':
    app.run()
