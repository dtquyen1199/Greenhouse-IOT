import serial
import pymysql
import paho.mqtt.publish as publish

device = '/dev/ttyS0'
    
arduino = serial.Serial(device,9600)

while True:
    lightRead = arduino.readline()
    print(lightRead)
    dbConn = pymysql.connect("localhost","pi","","lightReading_db") or die('Connection unsuccessful')
    publish.single("edge_device/data", lightRead, hostname="172.20.10.12")
    
    with dbConn:
        cursor = dbConn.cursor()
        cursor.execute("INSERT INTO lightLog (lightReading) VALUES(%s)"%(lightRead))
        dbConn.commit
        cursor.close()