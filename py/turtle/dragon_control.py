#turtle.py
# -*- coding:euc-kr -*-

import RPi.GPIO as GPIO
import lirc
import time
import os
import Adafruit_DHT
ON_OFF_POINT = 70

KEY_UP = "up"
KEY_DOWN = "down"
KEY_RIGHT = "right"
KEY_LEFT = "left"
KEY_UP_RIGHT = "upright"
KEY_UP_LEFT = "upleft"
KEY_DOWN_RIGHT = "downright"
KEY_DOWN_LEFT = "downleft"
KEY_F1 = "f1"
KEY_F2 = "f2"
KEY_F3 = "f3"
KEY_F4 = "f4"
KEY_F5 = "f5"
KEY_F6 = "f6"

goback_pwm_pin = 16  #GO, BACK PWM(SPEED) PIN
goback_dir_pin = 12  #GO, BACK DIRECTION PIN
lr_pwm_pin     = 19  #LEFT, RIGHT PWM(SPEED) PIN
lr_dir_pin     = 13  #LEFT, RIGHT DIRECTION PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(goback_pwm_pin, GPIO.OUT)
GPIO.setup(goback_dir_pin, GPIO.OUT)
GPIO.setup(lr_pwm_pin,     GPIO.OUT)
GPIO.setup(lr_dir_pin,     GPIO.OUT)

lr_speed = GPIO.PWM(lr_pwm_pin, 500)
lr_speed.start(0)

print("Smart Turtle Ship started")

socketid = lirc.init("irtest", blocking=False)
usb_control_file      = '/home/pi/py/turtle/files/usb.conf'
movement_control_file = '/home/pi/py/turtle/files/move.conf'
humid_control_file    = '/home/pi/py/turtle/files/humid.conf'
cannon_control_file   = '/home/pi/py/turtle/files/cannon.conf'
dragon_control_file   = '/home/pi/py/turtle/files/dragon.conf'

# USB Initialize
try:
    fout = open(usb_control_file, 'w')
    fout.write("USB_ON\n")
    fout.close()
    os.system("sudo /home/pi/py/hub-ctrl -h 0 -P 2 -p 1")
    print("USB Conf. has been initialized.")
except IOError:
    print("Cannot find file: " + usb_control_file)


def changeUSBState():
    try:
        fin = open(usb_control_file, 'r')
        usb_flag = fin.read()
        fin.close()
    
    except IOError:
        print("file read error")
    
    if usb_flag[0:6] == "USB_ON":
        os.system("sudo /home/pi/py/hub-ctrl -h 0 -P 2 -p 0")

        try:
            fout = open(usb_control_file, 'w')
            fout.write("USB_OFF\n")
            fout.close()

            fout = open(humid_control_file, 'w')
            fout.write("HUMID_OFF\n")
            fout.close()

            print("USB ON->OFF")
            print("Humidifier ON->OFF")
        except IOError:
            print("Cannot find file: " + usb_control_file)
    else :
        os.system("sudo /home/pi/py/hub-ctrl -h 0 -P 2 -p 1")
        
        try:
            fout = open(usb_control_file, 'w')
            fout.write("USB_ON\n")
            fout.close()

            fout = open(humid_control_file, 'w')
            fout.write("HUMID_ON\n")
            fout.close()

            print("USB OFF->ON")
            print("Humidifier OFF->ON")
        except IOError:
            print("Cannot find file: " + usb_control_file)

def changeAutoManualState():
    try:
        fin = open(movement_control_file, 'r')
        move_flag = fin.read()
        fin.close()
    
    except IOError:
        print("file read error")
    
    if move_flag[0:9] == "MOVE_AUTO":
        try:
            fout = open(movement_control_file, 'w')
            fout.write("MOVE_MANUAL\n")
            fout.close()
            print("Movement AUTO->MANUAL")
        except IOError:
            print("Cannot find file: " + movement_control_file)
    else :
        os.system("sudo /home/pi/py/hub-ctrl -h 0 -P 2 -p 1")

        try:
            fout = open(movement_control_file, 'w')
            fout.write("MOVE_AUTO\n")
            fout.close()
            print("MOVE MANUAL->AUTO")
        except IOError:
            print("Cannot find file: " + movement_control_file)

try:
    while(True):
        
        codeIR = lirc.nextcode()
        
        if len(codeIR) != 0 :
            print codeIR
            
            #Go
            if codeIR[0] == KEY_UP:
                print "KEY_UP pressed"
                GPIO.output(goback_pwm_pin, True)
                GPIO.output(goback_dir_pin, False)

            #Back
            elif codeIR[0] == KEY_DOWN:
                print "KEY_DOWN pressed"
                GPIO.output(goback_pwm_pin, True)
                GPIO.output(goback_dir_pin, True)

            #Left
            elif codeIR[0] == KEY_LEFT:
                print "KEY_LEFT pressed"
                lr_speed.ChangeDutyCycle(40) 
                GPIO.output(lr_dir_pin, False)

            #RIGHT
            elif codeIR[0] == KEY_RIGHT:
                print "KEY_RIGHT pressed"
                lr_speed.ChangeDutyCycle(40) 
                GPIO.output(lr_dir_pin, True)

            #Go, Left
            elif codeIR[0] == KEY_UP_LEFT:
                print "KEY_UP_LEFT pressed"
                GPIO.output(goback_pwm_pin, True)
                GPIO.output(goback_dir_pin, False)
                lr_speed.ChangeDutyCycle(70) 
                GPIO.output(lr_dir_pin, False)
            
            #Go, Right
            elif codeIR[0] == KEY_UP_RIGHT:
                print "KEY_UP_RIGHT pressed"
                GPIO.output(goback_pwm_pin, True)
                GPIO.output(goback_dir_pin, False)
                lr_speed.ChangeDutyCycle(70) 
                GPIO.output(lr_dir_pin, True)
            
            #Back, Left
            elif codeIR[0] == KEY_DOWN_LEFT:
                print "KEY_DOWN_LEFT pressed"
                GPIO.output(goback_pwm_pin, True)
                GPIO.output(goback_dir_pin, True)
                lr_speed.ChangeDutyCycle(70) 
                GPIO.output(lr_dir_pin, False)
            
            #Back, Right
            elif codeIR[0] == KEY_DOWN_RIGHT:
                print "KEY_DOWN_RIGHT pressed"
                GPIO.output(goback_pwm_pin, True)
                GPIO.output(goback_dir_pin, True)
                lr_speed.ChangeDutyCycle(70) 
                GPIO.output(lr_dir_pin, True)
            
            #USB On/Off
            elif codeIR[0] == KEY_F1:
                print "KEY_F1 pressed"
                changeUSBState()
            
            #Dragon Sound
            elif codeIR[0] == KEY_F2:
                print "KEY_F2 pressed"
                try:
                    fout = open(dragon_control_file, 'w')
                    fout.write("DRAGON_ON\n")
                    fout.close()

                    print("DRAGON OFF->ON")
                except IOError:
                    print("Cannot find file: " + cannon_control_file)

            #Cannon Sound
            elif codeIR[0] == KEY_F3:
                print "KEY_F3 pressed"
                try:
                    fout = open(cannon_control_file, 'w')
                    fout.write("CANNON_ON\n")
                    fout.close()

                    print("CANNON OFF->ON")
                except IOError:
                    print("Cannot find file: " + cannon_control_file)

            #USB(Humidifier/Light) Mode Change(Manual <-> Auto)
            elif codeIR[0] == KEY_F4:
                print "KEY_F4 pressed"
                changeAutoManualState()

            elif codeIR[0] == KEY_F5:
                print "KEY_F5 pressed"
            elif codeIR[0] == KEY_F6:
                print "KEY_F6 pressed"
            
            time.sleep(0.35)
            GPIO.output(goback_pwm_pin, False)
            lr_speed.ChangeDutyCycle(0) 
        
        time.sleep(0.01)

except KeyboardInterrupt:
    lirc.deinit()

finally:
    print ""
    GPIO.cleanup()

    os.system("sudo /home/pi/py/hub-ctrl -h 0 -P 2 -p 1")
    print("Program End")


