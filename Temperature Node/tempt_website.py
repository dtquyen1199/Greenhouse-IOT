import serial
import time
import pymysql
from flask import Flask, render_template, request
import Adafruit_DHT as dht


app = Flask(__name__)

DHT11_pin = 0

#Dictionary of digital pins 
pins = {
    2 : {'name' : 'Green LED', 'state' : 0},
    4 : {'name' : 'Red LED', 'state' : 0},
    7 : {'name' : 'FAN', 'state' : 0}
    }


@app.route("/")
def index ():
    #data send to index.html
    templateData = {'pins' : pins}
   
    return render_template ('index.html', **templateData)


@app.route("/<pin>/<state>")

def state(pin, state):    
    
    pin = int(pin)
    
    device = pins[pin]['name']
    
    if state == "on":        
        if pin == 2:
            ser.write(b"one\n")
            pins[pin]['state'] = 1
        if pin == 4:
            ser.write(b"three\n")
            pins[pin]['state'] = 1
        if pin == 7:
            ser.write(b"five\n")
            pins[pin]['state'] = 1
    
    if state == "off":        
        if pin == 2:
            ser.write(b"two\n")
            pins[pin]['state'] = 0
        if pin == 4:
            ser.write(b"four\n")
            pins[pin]['state'] = 0
        if pin == 7:
            ser.write(b"six\n")
            pins[pin]['state'] = 0
        
    if state == "low":        
        if pin == 7:
            ser.write(b"low\n")
            pins[pin]['state'] = 1
        
    if state == "medium":        
        if pin == 7:
            ser.write(b"medium\n")
            pins[pin]['state'] = 1
        
    if state == "high":        
        if pin == 7:
            ser.write(b"high\n")
            pins[pin]['state'] = 1
           
    
    templateData = {'pins' : pins}
   
   
    return render_template('index.html', **templateData)

@app.route("/<action>")

def action(action):
    if action == 'action1':
        ser.write(b"one\n")
        pins[2]['state'] = 1
    if action == 'action2':
        ser.write(b"two\n")
        pins[2]['state'] = 0
    if action == 'action3':
        ser.write(b"three\n")
        pins[4]['state'] = 1
    if action == 'action4':
        ser.write(b"four\n")
        pins[4]['state'] = 0
    if action == 'action5':
        ser.write(b"five\n")
        pins[7]['state'] = 1
    if action == 'action6':
        ser.write(b"six\n")
        pins[7]['state'] = 0
    if action == 'action7':
        ser.write(b"low\n")
        pins[7]['state'] = 1
    if action == 'action8':
        ser.write(b"medium\n")
        pins[7]['state'] = 1
    if action == 'action9':
        ser.write(b"high\n")
        pins[7]['state'] = 1
   
    templateData = {'pins' : pins}
   
    return render_template('index.html', **templateData)

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)
    ser.flush()
    app.run(debug = True, host = '0.0.0.0' , port = 80)


