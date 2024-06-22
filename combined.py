import grovepi
import paho.mqtt.client as mqtt
import time
import json
import math

# Connect the DHT22 sensor to digital port D4
dht_sensor_port = 2

# Set up the ultrasonic sensor ports
ultrasonic_ranger_1 = 7  # D7
ultrasonic_ranger_2 = 8  # D8

# MQTT settings
broker = "192.168.0.160"
port = 1883
temp_humidity_topic = "home/room1/temperature_humidity"
people_count_topic = "home/room1/people_count"

# Initialize MQTT client
client = mqtt.Client()
client.connect(broker, port, 60)

count = 0
state1 = True
state2 = True
i = 1

def read_ultrasonic(sensor):
    try:
        return grovepi.ultrasonicRead(sensor)
    except TypeError:
        return -1
    except IOError:
        return -1

while True:
    try:
        # Read temperature and humidity data
        [temp, humidity] = grovepi.dht(dht_sensor_port, 0)
        if not (math.isnan(temp) or math.isnan(humidity)):
            # Create payload
            temp_humidity_payload = json.dumps({"temperature": temp, "humidity": humidity})
            # Publish to MQTT broker
            client.publish(temp_humidity_topic, temp_humidity_payload)
            #print(f"Published: {temp_humidity_payload}")

        # Read ultrasonic sensor data
        distance1 = read_ultrasonic(ultrasonic_ranger_1)
        distance2 = read_ultrasonic(ultrasonic_ranger_2)
        
        if distance1 > 0 and distance1 < 20 and i == 1 and state1:
            # Object detected by sensor 1 and expecting it
            state1 = False
            time.sleep(0.1)
            i += 1

        elif distance2 > 0 and distance2 < 20 and i == 2 and state2:
            # Object detected by sensor 2 and expecting it
            print("Entering inside the room")
            state2 = False
            time.sleep(0.1)
            i = 1
            count += 1
            print("No. of people inside room: ", count)
            if not math.isnan(count):
                client.publish(people_count_topic, str(count))
                print("Data Sent using MQTT")

        elif distance2 > 0 and distance2 < 20 and i == 1 and state2:
            # Object detected by sensor 2 first, indicating exiting sequence
            state2 = False
            time.sleep(0.1)
            i = 2

        elif distance1 > 0 and distance1 < 20 and i == 2 and state1:
            # Object detected by sensor 1 indicating exit complete
            print("Exiting from room")
            state1 = False
            time.sleep(0.1)
            count -= 1
            print("No. of people inside room: ", count)
            i = 1
            if not math.isnan(count):
                client.publish(people_count_topic, str(count))
                print("Data Sent using MQTT")

        if distance1 >= 20:
            state1 = True
        if distance2 >= 20:
            state2 = True

        time.sleep(0.1)
    except IOError:
        print("Error reading from sensors")
    except KeyboardInterrupt:
        print("Terminating program")
        break
