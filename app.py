from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pywebhdfs.webhdfs import PyWebHdfsClient
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/uploadfile', methods=['POST'])
def uploadFile():
    dataDict={}
    if request.method == 'POST':
        file = request.files['file']
        timestamp = int(datetime.datetime.now().timestamp())
        # filename = secure_filename(str(timestamp) +'-'+ file.filename)
        filename = secure_filename("data-"+str(timestamp))
        my_file = '/ftp-files/' + filename
        hdfs = PyWebHdfsClient(host='192.168.1.11',port='50070', user_name='hduser')
        saved = hdfs.create_file(my_file, file)
        if saved:
            dataDict['status'] = 'SUCCESS'
            dataDict['response'] = my_file
            dataDict['message'] = 'File uploaded successfully'
            return dataDict
        else:
            dataDict['status'] = 'FAIL'
            dataDict['response'] = ''
            dataDict['message'] = 'File not uploaded'
            return dataDict

# main driver function 
if __name__ == '__main__':
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(host='192.168.1.11', port='5000', debug=True) 
