from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
#from flask import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas as pd
import csv
import json
import os
import requests



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

@app.route('/', methods= ['GET', 'POST'])
def index():
    return render_template("index.html")

#View input in brackets
@app.route('/data', methods= ['GET', 'POST'])
def data():
    if request.method == 'POST':
        f = request.form['csvfile']
        data = []
        with open(f) as file:
            csvfile = csv.reader(file)
            for row in csvfile:
                data.append(row)
        data = pd.DataFrame(data)
        return render_template('data.html', data=data.to_html())

#fileUploads= "/Users/gerardcarthy/Desktop/summerProjectCode/gcSummerProject/static/fileUploads"

app.config["FILE_UPLOADS"] = "/Users/gerardcarthy/Desktop/summerProjectCode/gcSummerProject/static/fileUploads"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["CSV","JSON"]
app.config['SECRET_KEY'] = '1234556'

#verify Files as CSV or JSON
def allowed_files(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False

#local File Load
@app.route("/loader", methods =["GET","POST"])
def upload_file():
    #Uploads file to folder locally
    if request.method == "POST":
        print(request.files)
        oclfile = request.files["file"]
            
        if oclfile.filename == "":
            flash("Upload must have a filename")
            return redirect(request.url)
        
        if not allowed_files(oclfile.filename):
            flash("This file extension is not allowed, please use csv or json file", "error")
            return redirect(request.url)
        
        else: 
            filename = secure_filename(oclfile.filename)
            #oclfile.save(os.path.join(app.config["FILE_UPLOADS"], oclfile.filename))

        flash("File Saved")
        flash("Ready for new upload")

        return redirect(request.url)
    
    return render_template("loader.html")


#Authorization Token c3b42623c04c87e266d12ae0e297abbce7f1cbe8
"""Import Begins 
{
    "state": "STARTED",
    "task": "dc4ef66f-449c-44de-9b83-c1e4a078c9eb-datim-admin"
}
Import Completed
Processed 28 of 28 -- 28 NEW (200:4, 201:24)
Exception Raised
{
    "exception": "task dc4ef66f-449c-44de-9b83-c1e4a078c9eb-datim-admi not found"
}
payload = {}
headers= {}
response = requests.request("GET", url, headers=headers, data = payload)
print(response.text.encode('utf8'))
QA Token a28072a2eb82c6c9949ba6bb8489002438e5bcc7
"""

""" def status():
    url = "https://api.qa.openconceptlab.org/manage/bulkimport/?task=ff5ce807-9833-4c7b-aa64-f89bc5a9a368-pritam-default&result=summary"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    return response, render_template("upload.html") """

app.config["FILE_UPLOADS"] = "/Users/gerardcarthy/Desktop/summerProjectCode/gcSummerProject/static/fileUploads"
@app.route("/upload", methods= ["GET","POST"])
def upload():
    if request.method == "POST":
        print(request.files)
        oclfile = request.files["file"]
        content = request.files['file'].read()
            
        if oclfile.filename == "":
            flash("Upload must have a filename")
            return redirect(request.url)
        
        if not allowed_files(oclfile.filename):
            flash("This file extension is not allowed, please use csv or json file", "error")
            return redirect(request.url)
        
        else:
            url = 'http://api.qa.openconceptlab.org/manage/bulkimport'
            filename = secure_filename(oclfile.filename)
            #oclfile.post(url, data=json.dumps(payload))
            #print(content)
            with open(os.path.join(app.config["FILE_UPLOADS"], filename), "wb") as fp:
                fp.write(content)
                headers = {'Content-type': 'text/html; charset=UTF-8', "Authorization": "Token hZrdvmAT7FvHXSLUqcz2WAH4GTm5sj"}
                requests.post(url, files={filename:content})
                #response = requests.get(url, files={filename:content})

        flash("Processed")
        flash("Ready for new upload")
        #flash(response)

        return redirect(request.url)
    
    return render_template("upload.html")

    #def status():
        #if request.method=="GET":
            #oclfile = request["status"]
            #url = "https://api.qa.openconceptlab.org/manage/bulkimport/?task=ff5ce807-9833-4c7b-aa64-f89bc5a9a368-pritam-default&result=summary"
            #payload = {}
            #headers= {"Authorization", "Token hZrdvmAT7FvHXSLUqcz2WAH4GTm5sj"}
            #response = requests.request(url, headers=headers)
            #flash(response)
            #return render_template("upload.html")
        #return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)