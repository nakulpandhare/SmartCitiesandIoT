#grovepi_Icd_dht.py
# This is an project for using the Grove OLED Display and the Grove DHT Sensor from
# the GrovePi starter kit
# In this project, the Temperature and humidity from the DHT sensor is printed on the DHT sensor 

from grovepi import * 
from grove_rgb_lcd import *
import time

dht_sensor_port = 2
# Connect the DHt sensor to port 2
while True:
    try:
        [temp, hum] = dht(dht_sensor_port, 0)  #Get the temperature and Humidity from the DHT sensor
        print "temp =", temp, "C\thumadity =", hum, "%"
	t = str (temp)
        h = str (hum)
        setRGB(0,125,64)
        #setRGB(0,255,0)
        setText("Temp:" + t + "C      " + "Humidity :" + h + "%")
    except (IOError, TypeError) as e:
        print "Error"
    
    time.sleep(2)
