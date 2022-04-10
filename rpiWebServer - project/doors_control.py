import time
import board
import RPi.GPIO as GPIO
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017
from alarm_control import pin_alarm
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
i2c = busio.I2C(board.SCL, board.SDA)
expander = MCP23017(i2c)
buzzer = 0
pin_phase = 0 ## 1 - start checking pin, 2 - first digit correct, 3 - second digit correct, 4 - third digit correct, 5 - PIN correct
first_digit = "1"
second_digit = "2"
third_digit = "3"
fourth_digit = "4"
doors_opened = 0
global key
key = 0
servo = 18
GPIO.setup(servo,GPIO.OUT)
doors=GPIO.PWM(servo,50)
doors.start(2.5) ## Dutycycle: 2.5 - doors closed, 7.5 - doors opened
GPIO.setup(buzzer, GPIO.OUT)
### 0-7 GPA (prawa strona)
## 8-15 GPB (lewa strona)
pin7=expander.get_pin(12)
pin7.switch_to_output(value=False)
pin6=expander.get_pin(13)
pin6.switch_to_output(value=False)
pin5=expander.get_pin(14)
pin5.switch_to_output(value=False)
pin4=expander.get_pin(15)
pin4.switch_to_output(value=False)
pin3=expander.get_pin(8)
pin3.switch_to_input(value=False)
pin2=expander.get_pin(9)
pin2.switch_to_input(value=False)
pin1=expander.get_pin(10)
pin1.switch_to_input(value=False)
pin0=expander.get_pin(11)
pin0.switch_to_input(value=False)
R1 = pin7
R2 = pin6
R3 = pin5
R4 = pin4
C1 = pin3
C2 = pin2
C3 = pin1
C4 = pin0
def correctkeypressed():
            GPIO.output(buzzer, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(buzzer, GPIO.LOW)   

def readLine(row, characters):
    global key
    row.value=True
    if(pin0.value == 1):
        key=characters[0]
    if(pin1.value == 1):
        key=characters[1]
    if(pin2.value == 1):
        key=characters[2]
    if(pin3.value == 1):
        key=characters[3]
    row.value=False
    print(key)
    return key       
try:
    while True:
        doors.ChangeDutyCycle(0)
        key = readLine(R1, ["1","2","3","A"])
        key = readLine(R2, ["4","5","6","B"])
        key = readLine(R3, ["7","8","9","C"])
        key = readLine(R4, ["*","0","#","D"])
        if (pin_phase == 0 and key=="D"):
            GPIO.output(buzzer, GPIO.HIGH)
        if (pin_phase == 0 and key!="D"):
            GPIO.output(buzzer, GPIO.LOW)
        if (pin_phase == 0 and key=="*"):
            pin_phase = 1
            correctkeypressed()
            key = '...'
        if (pin_phase == 1 and key!=first_digit and key!='...'):
            pin_alarm()
            pin_phase = 0
            key = '...'
        if (pin_phase == 1 and key==first_digit):
            pin_phase = 2
            correctkeypressed()
            key = '...'
        if (pin_phase == 2 and key!=second_digit and key!='...'):
            pin_alarm()
            pin_phase = 0
            key = '...'
        if (pin_phase == 2 and key==second_digit):
            pin_phase = 3
            correctkeypressed()
            key = '...'
        if (pin_phase == 3 and key!=third_digit and key!='...'):
            pin_alarm()
            pin_phase = 0
            key = '...'
        if (pin_phase == 3 and key==third_digit):
            pin_phase = 4
            correctkeypressed()
            key = '...'
        if (pin_phase == 4 and key!=fourth_digit and key!='...'):
            pin_alarm()
            pin_phase = 0
            key = '...'
        if (pin_phase == 4 and key==fourth_digit):
            doors.ChangeDutyCycle(7.5)
            time.sleep(1)
            doors.ChangeDutyCycle(0)
            pin_phase = 0
            doors_opened = 1
            correctkeypressed()
            key = '...'
        if (doors_opened == 1 and key=="C"):
            doors.ChangeDutyCycle(2.5)
            time.sleep(1)
            doors.ChangeDutyCycle(0)  
            doors_opened = 0
            correctkeypressed()
            key = '...'
            
        
except KeyboardInterrupt:
    print("\nApplication stopped!")
    
