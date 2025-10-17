from flask import Flask, request
import pandas as pd

app = Flask(__name__)

# /upload page will output the following
@app.route('/upload', methods=['POST'])
def upload():
    # requests file from html file with name of csvSheet
    file = request.files['csvSheet']
    df = pd.read_csv(file)
    print(df) 
    # flask needs to return something that the web browser can understand (txt/html)
    return df.to_html()

app.run()