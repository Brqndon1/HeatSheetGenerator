from flask import Flask, request, render_template_string
import csv
import io

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Enter your Sheet</h1>
    <h3>Please upload your csv file</h3>

    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="csvSheet" accept=".csv">
        <button type="submit">Upload</button>
    </form>

    <img src="image.png" alt="Swimming Icon">
    '''

@app.route("/upload", methods=['POST'])
def upload():
    print("Success!")
    return "File upload successful"
