from flask import Flask, request, send_file
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
    fastest3 = request.form.get("fastest3")

    if stroke:
        df = df[df["stroke"] == stroke]

    if ageGroup:
        df = df[df["age_group"] == ageGroup]

    if fastest3:
        df = df.sort_values("original_time").head(3)

    # makes df into excel format 
    # file is ready to be downloaded later in /upload
    df.to_excel('temp_results.xlsx', index=False)

    back_button = '<button onclick="history.back()">Back</button>'
    download_button = '<a href="/download_excel"><button>Download Excel</button></a>'

    # flask needs to return something that the web browser can understand (txt/html)
    return df.to_html() + back_button + download_button

# user wants to download results to excel
@app.route('/download_excel')
def download_excel():
    # sends file created in /upload to send from server to computer
    return send_file('temp_results.xlsx', as_attachment=True, download_name='heat_sheet_results.xlsx')

app.run()