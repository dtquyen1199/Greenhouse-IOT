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

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)
    ser.flush()
    arduino = serial.Serial(device, 9600)
    

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'PLm2zzGFjTgrKMn8Jw77'


INTERVAL = 2
sensor_data = {'moisture': 0, 'waterTankLevel': 0, 'pumpState': 0}
next_reading = time.time()
client = mqtt.Client()

client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST, 1883, 60)

    
    

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    payload = json.loads((msg.payload).decode("utf-8"))
    print payload
    if 'method' in payload and 'params' in payload:
        if payload['method'] == 'setValue' and payload['params'] != sensor_data['pumpState']:
            ser.write(b"1\n")
            ser.write(b"7\n")
            print("Pump State is changed")    

def getSensorData():
    data = arduino.readline()
    data = data.strip()
    dataList = data.split(",")
    return dataList
    
client.subscribe('v1/devices/me/rpc/request/+')




client.loop_start()
try:
    while True:
        latestData = getSensorData()
        print(latestData)
        sensor_data['moisture'] = latestData[0]
        sensor_data['waterTankLevel'] = latestData[1]
        if latestData[2] == "0":
            sensor_data['pumpState'] = False;
        else: sensor_data['pumpState'] = True;
        
        waterLvl = latestData[1]
        if waterLvl >= 10:
            ser.write(b"1\n")
        elif waterLvl < 10 and waterLvl >= 5:
            ser.write(b"2\n")        
        elif waterLvl < 5: 
            ser.write(b"3\n")
        
        print(sensor_data)
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        
        
        client.on_message = on_message
        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass


client.loop_stop()
client.disconnect()