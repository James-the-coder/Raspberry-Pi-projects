    #!/usr/bin/python
    # servoTest.py

import initio

# Define pins for Pan/Tilt
pan = 0
tilt = 1
tVal = 0 # 0 degrees is centre
pVal = 0 # 0 degrees is centre

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================


initio.init()
#print "Initio version: ", initio.version()

def doServos():
    initio.setServo(pan, pVal)
    initio.setServo(tilt, tVal)

   

    

# Initio Motor Test
# Moves: Forward, Reverse, turn Right, turn Left, Stop - then repeat
# Press Ctrl-C to stop
#
# Also demonstrates writing to the LEDs
#
# To check wiring is correct ensure the order of movement as above is correct
# Run using: sudo python motorTest.py


import initio, time

#======================================================================
# Reading single character by forcing stdin to raw mode
import sys
import tty
import termios

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)  # 16=Up, 17=Down, 18=Right, 19=Left arrows

# End of single character reading
#======================================================================

speed = 60

print "Tests the motors by using the arrow keys to control"
print "Use , or < to slow down"
print "Use . or > to speed up"
print "Speed changes take effect when the next arrow key is pressed"
print "Press Ctrl-C to end"
print

initio.init()
button = True
# main loop
try:
    while True:
            keyp = readkey()
            while button:
                    
                    
                if keyp == 'w' or ord(keyp) == 16:
                    distance = initio.getDistance()
                    initio.forward(70)   
                    if distance <  10:
                        initio.stop()         
                                    
                        tVal = 16
                        pVal = 0
                        doServos()
                                         
                                    
                        tVal = -75
                        pVal = 0
                        doServos()
                        print "Left", tVal, pVal
                        distLeft = initio.getDistance()
                        time.sleep(2)
                                   
                        tVal = 90
                        pVal = 0
                        doServos()
                        print "Right", tVal, pVal
                        distRight = initio.getDistance()
                        time.sleep(2)
                        tVal = 16
                        pVal = 0
                        doServos() 
                        print 'alert'
                        initio.reverse(70)
                        time.sleep(0.5)
                        if distLeft < distRight:
                            initio.reverse(70)
                            time.sleep(1)
                            initio.spinLeft(100)
                            time.sleep(1)
                        if distRight < distLeft:
                            initio.reverse(70)
                            time.sleep(0.5)
                            initio.spinRight(100)
                            time.sleep(1)
                               

                            
                elif keyp == ' ':
                        initio.stop()
                        print 'Stop'
                elif ord(keyp) == 3:
                        break


except KeyboardInterrupt:
        print

finally:
    initio.cleanup()
        
