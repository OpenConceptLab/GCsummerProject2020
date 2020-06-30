from flask import Flask, render_template, url_for, request, redirect, flash
#from flask import SQLAlchemy
from werkzeug.utils import secure_filename
import pandas as pd
import csv
import json
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""


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

#fileUploads= "/Users/gerardcarthy/Desktop/summerProjectCode/gcSummerProject/static/fileUploads"

app.config["FILE_UPLOADS"] = "/Users/gerardcarthy/Desktop/summerProjectCode/gcSummerProject/static/fileUploads"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["CSV","JSON"]
app.config['SECRET_KEY'] = '1234556'

def allowed_files(filename):
    if not "." in filename:
        return False
    
    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/loader", methods =["GET","POST"])
def upload_file():
    flash("working")
    if request.method == "POST":
        print(request.files)
        oclfile = request.files["file"]
            
        if oclfile.filename == "":
            flash("Upload must have a filename")
            return redirect(request.url)
        
        if not allowed_files(oclfile.filename):
            flash("This file extension is not allowed, please use csv or json file")
            return redirect(request.url)
        
        else: 
            filename = secure_filename(oclfile.filename)
            oclfile.save(os.path.join(app.config["FILE_UPLOADS"], oclfile.filename))

        flash("File Saved")

        return redirect(request.url)
    
    return render_template("loader.html")


if __name__ == "__main__":
    app.run(debug=True)