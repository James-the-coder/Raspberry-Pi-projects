import RPi.GPIO as GPIO
from picamera import PiCamera
from datetime import datetime


import time
GPIO.setmode(GPIO.BCM)
camera = PiCamera()
camera.rotation = 180

PIR_PIN = 4
GPIO.setup(PIR_PIN, GPIO.IN)


try:
    print("PIR Module Test(cntrl-c to exit)")
    time.sleep(2)
    print("Ready")
    while True:
        if GPIO.input(PIR_PIN):
            
            print("motion detected!!")
            filename = datetime.now().strftime("/home/pi/Documents/picamera/%y-%m-%d_%h.%m.%s.h264")
            camera.start_recording(filename)
            camera.start_preview()
            time.sleep(3)
            camera.stop_recording()
            camera.stop_preview()
            
             
            print("captured")
            time.sleep(1)
        
except KeyboardInterrupt:
    print(" Quit")
    GPIO.cleanup()
    
