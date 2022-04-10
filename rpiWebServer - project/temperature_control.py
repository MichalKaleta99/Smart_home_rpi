import w1thermsensor
import RPi.GPIO as GPIO
import os
import time
import sys
import Adafruit_DHT
from gpiozero import MCP3008
import busio
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from alarm_control import switch_alarm
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
spi.max_speed_hz=1000000
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs)
potentiometer = AnalogIn(mcp, MCP.P0)
fan_fdbck = AnalogIn(mcp, MCP.P1)
switch = AnalogIn(mcp, MCP.P4)
turnon_fan = 6 #INPUT1 - L293D
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(19, GPIO.OUT) #dioda grzejnika
GPIO.setup(turnon_fan, GPIO.OUT) #INPUT1
GPIO.setup(13, GPIO.OUT) #PWM FOR FAN
fan = GPIO.PWM(13, 100)
heating_led = GPIO.PWM(19,100) #(numer pinu, czestotliwosc wypelnienia)
user_interrupt = 0
switch_pressed = 0
min_temp_allowed = 16.0
max_temp_allowed = 26.0
temp_range = max_temp_allowed - min_temp_allowed  
sensor = w1thermsensor.W1ThermSensor()     
def temp_pv_function():
    temp_pv = sensor.get_temperature()
    temp_pv=round(temp_pv,1)
    return temp_pv   
def temp_control_automatic(temp_sp):
    global user_interrupt
    check_switch = switch_manual()
    temp_range = max_temp_allowed - min_temp_allowed
    temp_pv = temp_pv_function()
    if (temp_sp >= min_temp_allowed and temp_sp<temp_pv and check_switch == 0):
            GPIO.output(turnon_fan, GPIO.HIGH)
            while True:
                check_switch = switch_manual()
                temp_pv = temp_pv_function()
                difference_multiplier = 1+0.25*(temp_pv - temp_sp)
                fan_fill = 0.85*(temp_pv - min_temp_allowed)*difference_multiplier
                if(fan_fill>temp_range):
                    fan_fill = temp_range
                fan_fill = 100*(fan_fill/temp_range)
                fan_fill = int(fan_fill)
                fan.start(fan_fill)
                time.sleep(3)
                if user_interrupt == 1 or check_switch == 1:
                    user_interrupt = 0
                    break
    elif (temp_sp <= max_temp_allowed and temp_sp>temp_pv and check_switch == 0):
            while True:
                check_switch = switch_manual()
                temp_pv = temp_pv_function()
                difference_multiplier = 1+0.2*(temp_sp - temp_pv)
                heater_fill = 0.85*(max_temp_allowed - temp_pv)*difference_multiplier
                if(heater_fill>temp_range):
                    heater_fill = temp_range
                heater_fill = 100*(heater_fill/temp_range)
                heater_fill = int(heater_fill)
                heating_led.start(heater_fill)
                time.sleep(3)
                if user_interrupt == 1 or check_switch == 1:
                    break              
    elif check_switch == 1:
        switch_alarm()
def fan_manual(rpm):
    GPIO.output(turnon_fan, GPIO.HIGH)
    rpm = int(rpm)
    fan.start(rpm)
def heater_manual(heat_level):
    heat_level = int(heat_level)
    heating_led.start(heat_level)    
def switch_manual():
    if (switch.value>50000):
        switch_pressed = 1
    if (switch.value<=50000):
        switch_pressed = 0    
    while switch_pressed == 1:
        GPIO.output(turnon_fan, GPIO.HIGH)
        rpm = potentiometer.value/65535
        rpm = int(rpm)
        fan.start(rpm)
    return switch_pressed    
def temp_control_stop():
    global user_interrupt
    user_interrupt = 1
    GPIO.output(turnon_fan, GPIO.LOW)
    fan.stop()
    GPIO.output(19, GPIO.LOW)
    heating_led.stop()
fan_fdbck = AnalogIn(mcp, MCP.P1)
def fan_fdbck():
    fan_fdbck_percentage = fan_fdbck.value/65535
    fan_fdbck_percentage = int(fan_fdbck_percentage)
    return fan_fdbck_percentage
def main():
    try:
        while True:
           switch_manual()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
    pass
    
if __name__ == '__main__':
    main()

           