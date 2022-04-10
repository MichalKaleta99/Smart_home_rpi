import RPi.GPIO as GPIO
import os
import time
import socket
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(25, GPIO.OUT) #PWM
GPIO.setup(5, GPIO.OUT) #IN1 dla sterownika silnika
GPIO.setup(7, GPIO.OUT) #IN2 dla sterownika silnika
GPIO.setup(20, GPIO.IN)  #krancowka na poczatku
GPIO.setup(21, GPIO.IN)  #krancowka na koncu
pwm = GPIO.PWM(25, 100)
global last_keyname
SOCKPATH = "/var/run/lirc/lircd"
sock = None
def init_irw():
    global sock
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    print ('starting up on %s' % SOCKPATH)
    sock.connect(SOCKPATH)
def next_key():
    while True:
        data = sock.recv(128)
        data = data.strip()
        if data:
            break
    global words
    words = data.split()
    if (last_keyname == b'KEY_1') or (last_keyname == b'KEY_2'):
        words[2] = '...' 
    return words[2]
def gate(action):
        global user_interrupt
        global keyname
        if action == "on":
            user_interrupt = 0
            GPIO.output(5, GPIO.HIGH)
            while GPIO.input(20) == True:
                keyname = next_key()
                GPIO.output(5, GPIO.HIGH)
                GPIO.output(7, GPIO.LOW)
                pwm.start(60)
                if (GPIO.input(20) == False) or (user_interrupt == 1) or (keyname == b'KEY_2'):
                    gate('stop')
                    for x in range(0,2):
                        last_keyname = keyname
                        keyname = next_key()
                    break             
        if action == "off":
            user_interrupt = 0
            GPIO.output(7, GPIO.HIGH)
            while GPIO.input(21) == True:
                keyname = next_key()
                GPIO.output(7, GPIO.HIGH)
                GPIO.output(5, GPIO.LOW)
                pwm.start(60)
                if GPIO.input(21) == False or (user_interrupt == 1) or (keyname == b'KEY_1'):
                    gate('stop')
                    for x in range(0,2):
                        last_keyname = keyname
                        keyname = next_key()
                    break
        if action == "stop":
            user_interrupt = 1
            pwm.stop()
            GPIO.output(5, GPIO.LOW)
            GPIO.output(7, GPIO.LOW)
            print("stop")
            time.sleep(2)
            keyname = '...'
if __name__ == '__main__':
    last_keyname = '...'
    init_irw()
    keyname = next_key()
    while True:
        for x in range(0,2):
            last_keyname = '...'
            keyname = next_key()
        while (keyname == b'KEY_1'):
            keyname = '...'
            gate('on')
        while (keyname == b'KEY_2'):
            keyname = '...'
            gate('off')
