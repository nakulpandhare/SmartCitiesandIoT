import time
import grovepi
from gpiozero import AngularServo


# Connecting Light Sensor to pin A1
light_sensor = 2
# Connecting Led to pin D3
led_blue = 3
led_red = 4
servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
mapped_value = 0


grovepi.pinMode(led_blue,"OUTPUT")
time.sleep(1)

grovepi.pinMode(led_red,"OUTPUT")
time.sleep(1)


grovepi.analogWrite(led_blue,255)
grovepi.analogWrite(led_red,255)

i = 0

#Function to map light sensor values ( 0 to 780) to led brightness (0 to 255)
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    try:
       # print("Running ScIoT")
        light_intensity = grovepi.analogRead(light_sensor)

        if (light_intensity < 350):
            servo.angle = 90
        elif (light_intensity > 350):
            servo.angle = 0

        mapped_value = map_range(light_intensity, 780, 10, 0, 255)
        print(mapped_value)

        grovepi.analogWrite(led_blue,mapped_value)
        grovepi.analogWrite(led_red,mapped_value)

    except IOError:
        print("Error")
