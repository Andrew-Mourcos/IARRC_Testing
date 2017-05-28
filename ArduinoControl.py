from nanpy import Servo
from nanpy import ArduinoApi as A
import time

def servo_mtr(right_degrees, left_degrees):
    servo = Servo(pin=9)
    if (right_degrees - left_degrees) < 25:
        servo.write((right_degrees+left_degrees)/2)
        time.sleep(1)

    else:
        confused = 1
    return confused

def motor(right_degrees, left_degrees, confused):

    max_speed = 255

    if confused == True:
        speed = 50

    else:
        multiplier = (((right_degrees+left_degrees)/2)/90)
        speed = max_speed * multiplier

    A.digitalWrite(12, A.HIGH)  # forward direction
    A.digitalWrite(9, A.LOW)  # brakes off
    A.analogWrite(3, speed)
