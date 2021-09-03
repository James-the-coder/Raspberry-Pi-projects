# The Pins. Use Broadcom numbers.
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.
STEPS     = 0.2

###### END ######




import os
import sys
import termios
import tty
import pigpio
from time import *
import threading
import RPi.GPIO as GPIO

bright = 90
r = 255.0
g = 0.0
b = 0.0
button1_pin = 23
button2_pin = 5
a = 0


GPIO.setmode(GPIO.BCM)

GPIO.setup(button1_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

brightChanged = False
abort = False
state = True

pi = pigpio.pi()

def countdown():
        global my_timer
        
        
        for x in range(my_timer):
                my_timer = my_timer - 1
                sleep(1)
                print(x)
        print("time up")

def updateColor(color, step):
	color += step
	
	if color > 255:
		return 255
	if color < 0:
		return 0
		
	return color


def setLights(pin, brightness):
	realBrightness = int(int(brightness) * (float(bright) / 255.0))
	pi.set_PWM_dutycycle(pin, realBrightness)

while True:
        a = 0
        while a == 0:

                if (GPIO.input(23) == 1):
                        my_timer = 3300
                        a += 1

                if (GPIO.input(5) == 1):
                        my_timer = 1500
                        a += 1
        countdown_thread = threading.Thread(target = countdown)
        countdown_thread.start()

        setLights(RED_PIN, r)
        setLights(GREEN_PIN, g)
        setLights(BLUE_PIN, b)

        try:
                while my_timer > 0:
                                
                        if state and not brightChanged:
                                if r == 255 and b == 0 and g < 255:
                                        g = updateColor(g, STEPS)
                                        setLights(GREEN_PIN, g)
                                        if my_timer == 0:
                                                break
                                                
                                elif g == 255 and b == 0 and r > 0:
                                        r = updateColor(r, -STEPS)
                                        setLights(RED_PIN, r)
                                        if my_timer == 0:
                                                break
                                                
                                elif r == 0 and g == 255 and b < 255:
                                        b = updateColor(b, STEPS)
                                        setLights(BLUE_PIN, b)
                                        if my_timer == 0:
                                                break
                                                
                                elif r == 0 and b == 255 and g > 0:
                                        g = updateColor(g, -STEPS)
                                        setLights(GREEN_PIN, g)
                                        if my_timer == 0:
                                                break
                                                
                                elif g == 0 and b == 255 and r < 255:
                                        r = updateColor(r, STEPS)
                                        setLights(RED_PIN, r)
                                        if my_timer == 0:
                                                break
                                                
                                elif r == 255 and g == 0 and b > 0:
                                        b = updateColor(b, -STEPS)
                                        setLights(BLUE_PIN, b)
                                        if my_timer == 0:
                                                break

                setLights(RED_PIN, 0)
                setLights(GREEN_PIN, 0)
                setLights(BLUE_PIN, 0)

        except KeyboardInterrupt:
                setLights(RED_PIN, 0)
                setLights(GREEN_PIN, 0)
                setLights(BLUE_PIN, 0)
                pi.stop
