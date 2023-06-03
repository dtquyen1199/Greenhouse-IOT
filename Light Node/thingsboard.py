import os
import time
import sys
import pymysql
import paho.mqtt.client as mqtt
import json

import serial
import pymysql
import time
device = '/dev/ttyS0'

pins = {
    2 : {'name' : 'PIN 2', 'state' : 0}
    }

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)
    ser.flush()
    arduino = serial.Serial(device, 9600)
    

    


#THINGSBOARD_HOST = '172.20.10.11'
THINGSBOARD_HOST = 'demo.thingsboard.io' #home ip
#create new device here

ACCESS_TOKEN = 'vYdJdN5GhGp7EcCWkviU' #thiem

#ACCESS_TOKEN = '6UzUlbLWcgwYFE3tOAIh' #andrea

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL = 2
sensor_data = {'lightValue': 0, 'lightState': 0}
next_reading = time.time()
client = mqtt.Client()
#client.on_message = on_message
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

#def change_pump_state():
    
    

def on_message(client, userdata, msg):
    #global tempMessage
    #tempMessage = msg.payload.decode('utf8')
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads((msg.payload).decode("utf-8"))
    print payload
    if payload['method'] == 'setValue' and 'params' in payload:
        #if value diffrerent
        if payload['params'] != sensor_data['lightState']:
        #turn off pump
            if payload['params'] == False:
                # turn off the light
                ser.write(b"1\n") #manual
                ser.write(b"4\n")
                pins[2]['state'] = 0
                
            elif payload['params'] == True:
                #turn on the light
                ser.write(b"1\n") #manual
                
                ser.write(b"3\n")
                pins[2]['state'] = 1  
            print("Light State is changed")
            #json_load = json.loads(tempMessage)
            #for x in json_load:
            #    print ("%s: %d" % (x, json_load[x]))

def getSensorData():
    data = arduino.readline()
    data = data.strip()
    dataList = data.split(",")
    return dataList
    
#if action == 'action1':
#        ser.write(b"4")
#    if action == 'action2':
#        ser.write(b"5")
#    if action == 'action3':
#        ser.write(b"6")
    
#Edge server needs to request/sub to thingsboard!
client.subscribe('v1/devices/me/rpc/request/+')


client.loop_start()
try:
    while True:
        latestData = getSensorData()
        print(latestData)
        sensor_data['lightValue'] = latestData[0]
        if pins[2]['state'] == 1: #something different here?
            sensor_data['lightState'] = True;
        else: sensor_data['lightState'] = False;
        
        print(sensor_data)
        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        
        #request = {"method" : "getValue", "params" : ""}
        #client.publish('v1/devices/me/rpc/request/1', json.dumps(request),1)
        client.on_message = on_message
        #can't be empty
        
        
        
        #extract info from json file 
        
        
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass


client.loop_stop()
client.disconnect()