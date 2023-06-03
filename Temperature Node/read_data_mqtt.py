import serial
import time
import pymysql
import paho.mqtt.publish as publish


device = '/dev/ttyS0'
arduino = serial.Serial(device, 9600)

while True:
    data = arduino.readline()
    print(data)
    time.sleep(1)
    data = arduino.readline()
    print(data)
   
    pieces = data.split("\t") #split data to save it in different variables
   
    tempt = pieces[0]
    humi = pieces[1]
   
   
    dbConn = pymysql.connect("localhost", "pi", "", "energy_log_db") or die ("Connection unsuccessful")
       
    with dbConn:
        cursor = dbConn.cursor()
        cursor.execute("INSERT INTO temptlog (Temperature, Humidity) VALUES (%s, %s)" % (tempt, humi))
        dbConn.commit
        cursor.close()
        
            
    #publish.single("edge_device/data", tempt,  hostname = "172.20.10.12")
    publish.single("edge_device/data", humi,  hostname = "172.20.10.12")
    


