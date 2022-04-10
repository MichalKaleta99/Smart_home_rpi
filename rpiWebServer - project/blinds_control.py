import RPi.GPIO as GPIO
import os
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) #PWM
GPIO.setup(23, GPIO.OUT) #IN1 dla sterownika silnika
GPIO.setup(24, GPIO.OUT) #IN2 dla sterownika silnika
GPIO.setup(27, GPIO.IN)  #krańcówka na dole rolety
GPIO.setup(22, GPIO.IN)  #krańcówka
pwm = GPIO.PWM(17, 100)
def main():
    pass     
def blinds(action):
        if action == "on":
            GPIO.output(23, GPIO.HIGH)
            while GPIO.input(27) == True:
                GPIO.output(23, GPIO.HIGH)
                GPIO.output(24, GPIO.LOW)
                pwm.start(10)
            if GPIO.input(27) == False:
                GPIO.output(23, GPIO.LOW)
                GPIO.output(24, GPIO.LOW)
                pwm.stop()
        if action == "off":
            GPIO.output(24, GPIO.HIGH)
            while GPIO.input(22) == True:
                GPIO.output(24, GPIO.HIGH)
                GPIO.output(23, GPIO.LOW)
                pwm.start(40)
            if GPIO.input(22) == False:
                GPIO.output(24, GPIO.LOW)
                GPIO.output(23, GPIO.LOW)
                pwm.stop()
        if action == "stop":
            pwm.stop()
            GPIO.output(23, GPIO.LOW)
            GPIO.output(24, GPIO.LOW)       
if __name__ == '__main__':
    main()

