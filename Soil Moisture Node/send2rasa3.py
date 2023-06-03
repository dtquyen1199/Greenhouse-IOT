import paho.mqtt.publish as publish
import serial
import time
device = '/dev/ttyS0'

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout = 1)
    ser.flush()
    arduino = serial.Serial(device, 9600)

while True:
    data = arduino.readline()
    data.strip()
    list = data.split(",")
    data = list[0]
    print(data)
    publish.single("edge_device/data",data, hostname="172.20.10.8")

