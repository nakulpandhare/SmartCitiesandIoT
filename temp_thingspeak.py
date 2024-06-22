from grovepi import *
from grove_rgb_lcd import *
import time
import requests

# ThingSpeak settings
THINGSPEAK_API_KEY = '1UA9AKJ6RU9K0GPK'  # Replace with your ThingSpeak write API key
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

dht_sensor_port = 2
# Connect the DHT sensor to port 2
while True:
    try:
        [temp, hum] = dht(dht_sensor_port, 0)  # Get the temperature and Humidity from the DHT sensor
        print("temp =", temp, "C\thumidity =", hum, "%")
        t = str(temp)
        h = str(hum)
        setRGB(0, 125, 64)
        setText("Temp:" + t + "C      " + "Humidity :" + h + "%")
        
        # Send data to ThingSpeak
        response = requests.get(THINGSPEAK_URL, params={
            'api_key': THINGSPEAK_API_KEY,
            'field1': temp,
            'field2': hum
        })
        if response.status_code == 200:
            print("Data successfully sent to ThingSpeak")
        else:
            print("Failed to send data to ThingSpeak, response code:", response.status_code)
    except (IOError, TypeError) as e:
        print("Error:", e)
    
    time.sleep(5)  # ThingSpeak allows updates every 15 seconds, setting to 5 to be safe
