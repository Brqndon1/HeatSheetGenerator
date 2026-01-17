from flask import Flask, request, send_file, make_response, session
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
    amount_of_lanes = int(request.form.get("amount_of_lanes", 8))

    if stroke:
        df = df[df["stroke"] == stroke]

    if ageGroup:
        df = df[df["age_group"] == ageGroup]

    if fastest3:
        df = df.sort_values("original_time").head(3)

    back_button = '<button onclick="history.back()">Back</button>'
    print_button = '<button onclick="window.print()">Print</button>'

    
    # flask needs to return something that the web browser can understand (txt/html)
    return back_button + print_button + formatHeatSheet(createFormat(), df, amount_of_lanes)

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
def formatHeatSheet(events, df, lanes):
    output = "<h2>Swim Meet - Event List</h2>"
    ## example event: Girls 8 & Under 25yd Backstroke
    df['event_full'] = df['age_group']+" "+df['distance'].astype(str)+"yd "+df['stroke']

    eventNum = 1
    # loop through each possible event
    for event in events:
        # df of only swimmers who match the event we are currently looping through
        event_swimmers = df[df['event_full'] == event]
        event_swimmers = event_swimmers.sort_values('converted_time', ascending=False)

        # ensuring no empty events
        if len(event_swimmers) > 0:
            output += f"<h2><b>Event {eventNum}: {event}</b></h2>"    # creating format for each event
            num_swimmers = len(event_swimmers)
            num_heats = (num_swimmers + int(lanes) - 1) // int(lanes)
            
            remainder = num_swimmers % int(lanes)
            if remainder == 0:
                remainder = int(lanes)

            # Loop through each heat
            for heat_num in range(1, num_heats + 1):
                # in case first heat is not fully filled (depending on # of swimmers)
                if heat_num == 1:
                    start_idx = 0
                    end_idx = remainder
                # ensures that rest of heats are filled completely
                else:
                    start_idx = remainder + (heat_num - 2) * int(lanes)
                    end_idx = start_idx + int(lanes)

                heat_swimmers = event_swimmers.iloc[start_idx:end_idx]
                
                # Add heat header
                output += f"<h4>Heat {heat_num} of {num_heats}</h4>"
                # Start a table for alignment
                output += "<table style='border-collapse: collapse; margin-left: 20px;'>"
                
                # Loop through each swimmer in this heat
                for lane_num, (idx, swimmer) in enumerate(heat_swimmers.iterrows(), start=1):
                    # Format name as "Last, First"
                    last_first = f"{swimmer['last_name']}, {swimmer['first_name']}"
                    # Add table row with lane, name, age, team, time
                    output += f"""
                    <tr>
                        <td style='padding-right: 20px; text-align: right;'>{lane_num}</td>
                        <td style='padding-right: 30px; text-align: left;'>{last_first}</td>
                        <td style='padding-right: 30px; text-align: left;'>{swimmer['age']}</td>
                        <td style='padding-right: 30px; text-align: left;'>{swimmer['team']}</td>
                        <td style='text-align: left;'>{swimmer['converted_time']}</td>
                    </tr>
                    """
                
                # Close table
                output += "</table>"
            output+= "<br>"
            eventNum += 1
    return output

app.run()