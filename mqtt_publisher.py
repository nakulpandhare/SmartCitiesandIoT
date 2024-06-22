import paho.mqtt.client as mqtt
import time

# Define the MQTT broker details
broker_address = "localhost"  # Assuming the broker is running on the same machine
port = 1883  # Default MQTT port
topic = "test/topic"  # The topic to publish to

# Define the message
message = "Hello, Node-RED! How are you :)"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # Once connected, publish the message
        client.publish(topic, message)
        print(f"Message '{message}' published to topic '{topic}'")
    else:
        print("Failed to connect, return code %d\n", rc)

# The callback for when a PUBLISH message is sent to the server.
def on_publish(client, userdata, mid):
    print("Message has been published.")
    client.disconnect()  # Disconnect after publishing the message

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_connect and on_publish callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(broker_address, port)

# Start the loop
client.loop_start()

# Keep the script running for a short period to ensure the message is sent
time.sleep(5)

# Stop the loop and disconnect
client.loop_stop()
