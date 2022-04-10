import time
import RPi.GPIO as GPIO
from digitalio import Direction
from alarm_control import pin_alarm
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
servo = 18
GPIO.setup(servo,GPIO.OUT)
doors=GPIO.PWM(servo,50)
doors.start(2.5) ## Dutycycle: 2.5 - doors closed, 7.5 - doors opened
doors.ChangeDutyCycle(0)
def main():
    pass
def doors_control(action):
    if action == "on":
        doors.ChangeDutyCycle(7.5)
        time.sleep(1)
        doors.ChangeDutyCycle(0)
    if action == "off":
            doors.ChangeDutyCycle(2.5)
            time.sleep(1)
            doors.ChangeDutyCycle(0)
if __name__ == '__main__':
    main()
            