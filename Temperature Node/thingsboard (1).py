import os
import time
import sys
import pymysql
import paho.mqtt.client as mqtt
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Pnki0dkz25Lh3utRpbbD'

# Data capture and upload interval in seconds.
INTERVAL = 2

sensor_data = {'temperature': 0, 'humidity': 0}

next_reading = time.time() 

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

def getLatestTemptData():
    dbConn = pymysql.connect("localhost", "pi", "", "energy_log_db") or die ("Connection unsuccessful")
    try:
        cursor = dbConn.cursor()
        cursor.execute("SELECT * FROM temptlog WHERE 1 ORDER BY Date DESC LIMIT 10")
        result = cursor.fetchall()
        cursor.close()
    except:
        cursor.close()
        result = False;
    
    return result

client.loop_start()

try:
    while True:
        
        latestData = getLatestTemptData()
        temperature  = latestData[0][1]
        humidity = latestData[0][2]                     
        
        sensor_data['temperature'] = temperature
        sensor_data['humidity'] = humidity

        # Sending humidity and temperature data to ThingsBoard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()