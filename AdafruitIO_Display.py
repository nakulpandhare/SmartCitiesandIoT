from grovepi import *
from grove_rgb_lcd import *
import time
import requests


# Adafruit IO settings
ADAFRUIT_IO_USERNAME = 'nakul23'  # Replace with your Adafruit IO username
ADAFRUIT_IO_KEY = 'aio_rsuk65N23yqJVhnWfpzrRnH4ZnjW'  # Replace with your Adafruit IO key
ADAFRUIT_IO_FEED_TEMP = 'temperature'  # Replace with your temperature feed name
ADAFRUIT_IO_FEED_HUM = 'humidity'  # Replace with your humidity feed name
ADAFRUIT_IO_FEED_NumberOfPeople = 'numberofpeople'
ADAFRUIT_IO_URL = 'https://io.adafruit.com/api/v2/{}/feeds/{}/data'

dht_sensor_port = 2
# Connect the DHT sensor to port 2

while True:
    try:
        NumberOfPeopleinRoom = int(input("Enter Number of People: "))
        [temp, hum] = dht(dht_sensor_port, 0)  # Get the temperature and Humidity from the DHT sensor
        print("temp =", temp, "C\thumidity =", hum, "%")
        t = str(temp)
        h = str(hum)
        setRGB(125, 5, 120)
        setText("Temp:" + t + "C      " + "Humidity :" + h + "%")
        
        # Send data to Adafruit IO
        temp_response = requests.post(ADAFRUIT_IO_URL.format(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_FEED_TEMP),
                                      headers={'X-AIO-Key': ADAFRUIT_IO_KEY},
                                      data={'value': temp})
        
        hum_response = requests.post(ADAFRUIT_IO_URL.format(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_FEED_HUM),
                                     headers={'X-AIO-Key': ADAFRUIT_IO_KEY},
                                     data={'value': hum})
        
        NumberOfPeople_response = requests.post(ADAFRUIT_IO_URL.format(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_FEED_NumberOfPeople),
                                      headers={'X-AIO-Key': ADAFRUIT_IO_KEY},
                                      data={'value': NumberOfPeopleinRoom})

        if temp_response.status_code == 200 and hum_response.status_code == 200 and NumberOfPeople_response.status_code == 200:
            print("Data successfully sent to Adafruit IO")
        else:
            print("Failed to send data to Adafruit IO")
            print("Temperature response code:", temp_response.status_code, "Response:", temp_response.text)
            print("Humidity response code:", hum_response.status_code, "Response:", hum_response.text)
            print("Number of People response code:", NumberOfPeople_response.status_code, "Response:", NumberOfPeople_response.text)

    except (IOError, TypeError) as e:
        print("Error:", e)
    
    time.sleep(15)  # Adafruit IO has a rate limit, adjust accordingly
