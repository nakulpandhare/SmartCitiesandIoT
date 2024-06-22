import grovepi
import paho.mqtt.client as mqtt
import time
import json
import math

# Connect the DHT22 sensor to digital port D4
sensor_port = 2

# MQTT settings
broker = "192.168.0.160"
port = 1883
topic = "home/room1/temperature_humidity"

# Initialize MQTT client
client = mqtt.Client()
client.connect(broker, port, 60)

#while True:
try:
    # Read sensor data
    [temp, humidity] = grovepi.dht(sensor_port, 0)
    if not (math.isnan(temp) or math.isnan(humidity)):
        # Create payload
        payload = json.dumps({"temperature": temp, "humidity": humidity})
        # Publish to MQTT broker
    #message = str(temp)
        client.publish(topic, payload)
#print(temp)
        #print(f"Published: {payload}")
    time.sleep(10)
except IOError:
    print("Error reading from DHT22 sensor")
