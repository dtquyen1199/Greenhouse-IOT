import serial
import time
import pymysql
from flask import Flask, render_template, request
import Adafruit_DHT as dht


app = Flask(__name__)

#Dictionary of digital pins 
pins = {
    2 : {'name' : 'Grenn LED', 'state' : 0},
    4 : {'name' : 'Red LED', 'state' : 0},
    7 : {'name' : 'FAN', 'state' : 0}
    }

def connectToDatabase():
    dbConn = pymysql.connect("localhost", "pi", "", "energy_log_db") or die ("Connection unsuccessful")
    
    return dbConn;

def getLatestTemptData():
    dbConn = connectToDatabase()
    try:
        cursor = dbConn.cursor()
        cursor.execute("SELECT * FROM temptlog WHERE 1 ORDER BY Date DESC LIMIT 1")
        result = cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
        result = False;
    
    return result


@app.route("/")
def data ():
    #data send to index.html
    latestData = getLatestTemptData()
    lastDataTime = latestData[0][0]
    lastTemperature = latestData[0][1]
    lastHumidity = latestData[0][2]
    
   
    return render_template ('index.html', lastDataTime = lastDataTime, lastTemperature = lastTemperature, lastHumidity = lastHumidity)

@app.route("/pins")

def pinsData ():
    
    templateData = {'pins' : pins}
   
    return render_template ('index.html', **templateData)



@app.route('/<request>/', methods=['GET', 'POST'])

def request():
    if request.method =="POST":
        speed = request.form.get("speed")
        ser.write(str(val).encode('ascii'))
        
    templateData = {'pins' : pins}
    
    return render_template ('index.html')


@app.route("/<pin>/<state>")

def state(pin, state):    
    
    temperature = ''
    humidity = ''    
    
    if pin == "dhtpin" and state == "get":
        tempt, humdt = dht.read_retry(dht.DHT11, 8)
        tempt = '{0:0.1f}'.format(tempt)
        humdt = '{0:0.1f}'.format(humdt)
        temperature = 'Temperature: ' + tempt
        humidity = 'Humidity: ' + humdt
    
    temptData = {
        'temperature' : temperature,
        'humidity' : humidity
        }
    pin = int(pin)
    
    device = pins[pin]['name']
    
    if state == "on":        
        if pin == 2:
            ser.write(b"1")
            pins[pin]['state'] = 1
        if pin == 4:
            ser.write(b"3")
            pins[pin]['state'] = 1
        if pin == 7:
            ser.write(b"5")
            pins[pin]['state'] = 1
    
    if state == "off":        
        if pin == 2:
            ser.write(b"2")
            pins[pin]['state'] = 0
        if pin == 4:
            ser.write(b"4")
            pins[pin]['state'] = 0
        if pin == 7:
            ser.write(b"6")
            pins[pin]['state'] = 0
           
    
    templateData = {'pins' : pins}
   
   
    return render_template('index.html', **templateData)

@app.route("/<action>")

def action(action):
    if action == 'action1':
        ser.write(b"1")
        pins[2]['state'] = 1
    if action == 'action2':
        ser.write(b"2")
        pins[2]['state'] = 0
    if action == 'action3':
        ser.write(b"3")
        pins[4]['state'] = 1
    if action == 'action4':
        ser.write(b"4")
        pins[4]['state'] = 0
    if action == 'action5':
        ser.write(b"5")
        pins[7]['state'] = 1
    if action == 'action6':
        ser.write(b"6")
        pins[7]['state'] = 0    
   
    templateData = {'pins' : pins}
   
    return render_template('index.html', **templateData)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)
    ser.flush()
    app.run(debug = True, host = '0.0.0.0' , port = 8080)


