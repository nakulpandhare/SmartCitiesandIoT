import grovepi
import paho.mqtt.client as mqtt
import time
import json
import math

# Set up the sensor ports
ultrasonic_ranger_1 = 7  # D7
ultrasonic_ranger_2 = 8  # D8

count = 0
state1 = True
state2 = True
i = 1

# MQTT settings
broker = "192.168.0.160"
port = 1883
topic = "home/room1/people_count"

# Initialize MQTT client
client = mqtt.Client()
client.connect(broker, port, 60)


def read_ultrasonic(sensor):
    try:
        # return grovepi.ultrasonicRead(sensor)
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
                client.publish(topic, str(count))
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
                client.publish(topic, str(count))
                print("Data Sent using MQTT")

        if distance1 >= 20:
            state1 = True
        if distance2 >= 20:
            state2 = True

        time.sleep(0.1)
    except TypeError:
        return -1
    except IOError:
        return -1

#while True:
    # distance1 = read_ultrasonic(ultrasonic_ranger_1)
    # distance2 = read_ultrasonic(ultrasonic_ranger_2)
    
    # if distance1 > 0 and distance1 < 20 and i == 1 and state1:
    #     # Object detected by sensor 1 and expecting it
    #     state1 = False
    #     time.sleep(0.1)
    #     i += 1

    # elif distance2 > 0 and distance2 < 20 and i == 2 and state2:
    #     # Object detected by sensor 2 and expecting it
    #     print("Entering inside the room")
    #     state2 = False
    #     time.sleep(0.1)
    #     i = 1
    #     count += 1
    #     print("No. of people inside room: ", count)
    #     if not math.isnan(count):
    #         client.publish(topic, str(count))
    #         print("Data Sent using MQTT")

    # elif distance2 > 0 and distance2 < 20 and i == 1 and state2:
    #     # Object detected by sensor 2 first, indicating exiting sequence
    #     state2 = False
    #     time.sleep(0.1)
    #     i = 2

    # elif distance1 > 0 and distance1 < 20 and i == 2 and state1:
    #     # Object detected by sensor 1 indicating exit complete
    #     print("Exiting from room")
    #     state1 = False
    #     time.sleep(0.1)
    #     count -= 1
    #     print("No. of people inside room: ", count)
    #     i = 1
    #     if not math.isnan(count):
    #         client.publish(topic, str(count))
    #         print("Data Sent using MQTT")

    # if distance1 >= 20:
    #     state1 = True
    # if distance2 >= 20:
    #     state2 = True

    # time.sleep(0.1)
