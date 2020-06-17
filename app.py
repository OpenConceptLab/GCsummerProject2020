from flask import Flask, render_template, url_for, request, redirect
import pandas as pd
import csv
import json
import os

app = Flask(__name__)

@app.route('/', methods= ['GET', 'POST'])
def index():
    return render_template("index.html")

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

app.config['FILE_UPLOADS'] = "/Users/gerardcarthy/Desktop/summerProjectCode/gcSummerProject/static/fileUploads"

@app.route("/upload_file", methods =["GET","POST"])
def upload_file():
    if request.method == "POST":

        if request.files:

            oclfile = request.files["csvfile"]

            oclfile.save(os.path.join(app.config['FILE_UPLOADS'], ocl.filename))

            print("File Saved")

            return redirct(request.url)
    
    return render_template('index.html')

            

if __name__ == "__main__":
    app.run(debug=True)