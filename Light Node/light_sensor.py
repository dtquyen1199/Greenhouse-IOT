import serial
import time
import pymysql
from flask import Flask, render_template

app = Flask(__name__)

# Dictionary of pins with name of pin and state ON/OFF
pins = {
    2 : {'name' : 'PIN 2', 'state' : 0}
    }

def connectToDatabase():
    dbConn = pymysql.connect("localhost","pi","","lightReading_db") or die('Connection unsuccessful')
    return dbConn;

def getLatestReading():
    dbConn = connectToDatabase()
    try:
        cursor = dbConn.cursor()
        cursor.execute("SELECT * FROM lightLog WHERE 1 ORDER BY Date DESC LIMIT 1")
        result = cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
        result = False
    return result

latestData = getLatestReading()
latestTime = latestData[0][0]
latestReading = latestData[0][1]

# Main function when accessing the website
@app.route("/")
def index():
    # latestData = getLatestReading()
    # latestTime = latestData[0][0]
    # latestReading = latestData[0][1]
    manualMode = False;
    
    templateData = {
        'pins' : pins,
        'manualMode' : manualMode,
        'latestTime' : latestTime,
        'latestReading' : latestReading
    }

    return render_template('index.html', **templateData)

@app.route("/manualMode/<toggle>")
def manualMode(toggle):
    if toggle == "on":
        ser.write(b"1")
        manualMode = True
        # Save the status message to be passed into the template:
        message = "Turned manual mode on."
    if toggle == "off":
        ser.write(b"2")
        manualMode = False
        message = "Turned manual mode off."
    
    # This data will be sent to index.html (pins dictionary)
    templateData = {
        'pins' : pins,
        'manualMode' : manualMode,
        'latestTime' : latestTime,
        'latestReading' : latestReading
    }       
    
    return render_template('index.html', **templateData)

# Function with buttons that toggle depending on the status
@app.route("/<changePin>/<toggle>")
def toggle_function(changePin, toggle):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)

    #Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']

    # If the action part of the URL is "on", execute the code indented below:
    if toggle == "on":
        # Set the pin high:
        if changePin == 2:
            ser.write(b"3")
            pins[changePin]['state'] = 1
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if toggle == "off":
        # Set the pin low:
        if changePin == 2:
            ser.write(b"4")
            pins[changePin]['state'] = 0
        message = "Turned " + deviceName + " off."


    # This data will be sent to index.html (pins dictionary)
    templateData = {
        'pins' : pins,
        'manualMode' : manualMode,
        'latestTime' : latestTime,
        'latestReading' : latestReading
    }

    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)

# Function to send simple commands
@app.route("/<action>")
def action(action):
    if action == 'action1':
        ser.write(b"3")
        pins[2]['state'] = 1
    if action == 'action2':
        ser.write(b"4")
        pins[2]['state'] = 0
    if action == 'action3':
        ser.write(b"5")
    if action == 'action4':
        ser.write(b"6")
    if action == 'action5':
        ser.write(b"7")

    # This data will be sent to index.html (pins dictionary)
    templateData = {
        'pins' : pins,
        'manualMode' : manualMode,
        'latestTime' : latestTime,
        'latestReading' : latestReading
    }

    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)

# Main function, set up serial bus, indicate port for the web server,
# and start the service
if __name__ == "__main__":
    ser = serial.Serial("/dev/ttyS0", 9600, timeout=1)
    ser.flush()
    app.run(host='0.0.0.0', port=8080, debug=True)