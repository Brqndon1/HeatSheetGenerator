from flask import Flask, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# /upload page will output the following
@app.route('/upload', methods=['POST'])
def upload():
    # requests file from html file with name of csvSheet
    file = request.files['csvSheet']
    file.seek(0)    # reset file so you can reuse back button
    df = pd.read_csv(file)

    stroke = request.form.get("stroke")
    ageGroup = request.form.get("ageGroup")

    if stroke:
        df = df[df["stroke"] == stroke]

    if ageGroup:
        df = df[df["age_group"] == ageGroup]

    print(df) 
    back_button = '<button onclick="history.back()">Back</button>'
    # flask needs to return something that the web browser can understand (txt/html)
    return df.to_html() + back_button

app.run()