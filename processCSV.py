from flask import Flask, request, send_file, make_response
from flask_cors import CORS
import pandas as pd
import io

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

    back_button = '<button onclick="history.back()">Back</button>'
    download_button = '<a href="/download_excel"><button>Download Excel</button></a>'

    
    # flask needs to return something that the web browser can understand (txt/html)
    return formatHeatSheet(createFormat(), df) + back_button + download_button

# user wants to download results to excel
@app.route('/download_excel')
def download_excel():
    events = createFormat()

    # create df with all events and event numbers
    df = pd.DataFrame({
        "Event Number": range(1, len(events)+1),
        "Event Name": events
    })
    
    # create temp file in RAM instead of saving to disk 
    # virtual file that exists only while program runs
    output = io.BytesIO()

    # write to temp file (output) and use openpyxl library to create .xlsx format
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name = "Events")
    
    # read file from start as it is currently at the end of file
    output.seek(0)

    return send_file(output, 
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # tells browser its an excel file
                    as_attachment=True,                       # forces download, not open in browser
                    download_name='heat_sheet_events.xlsx')   # downloaded file name

# create list of all events possible
def createFormat():
    genders1 = ["Girls", "Boys"]
    genders2 = ["Women", "Men"]
    ageGroup1 = ["8 & Under", "9-10", "11-12", "13-14"]
    ageGroup2 = ["15-18"]
    listYds = ["25yd", "50yd", "100yd"]
    listOfStrokes = ["Backstroke", "Breaststroke", "Butterfly", "Freestyle"]

    events = []

    events += [f"{gender} {age} {distance} {stroke}"
                for gender in genders1
                for age in ageGroup1
                for distance in listYds
                for stroke in listOfStrokes]
    events += [f"{gender} {age} {distance} {stroke}"
                for gender in genders2
                for age in ageGroup2
                for distance in listYds
                for stroke in listOfStrokes]
    return events

# to view heats in current tab
def formatHeatSheet(events, df):
    output = "<h2>Swim Meet - Event List</h2>"
    ## example event: Girls 8 & Under 25yd Backstroke
    for eventNum, event in enumerate(events, start=1):
        output += f"<p>Event {eventNum}: {event}</p>"    # creating format for each event
        # concatenate in df to check against event to add swimmers.
        for idx, row in df.iterrows():
            swimmer = f"{row['age_group']} {row['distance']}yd {row['stroke']}"
            if event == swimmer:
                output += f"<p2> {row['first_name']} {row['last_name']}<br></p2>"

    return output

app.run()