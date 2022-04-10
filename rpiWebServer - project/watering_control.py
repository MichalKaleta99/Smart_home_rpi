import RPi.GPIO as GPIO
import os
import time
import sys
import Adafruit_DHT
import board
import busio
from digitalio import Direction
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
expander = MCP23017(i2c)
blue_led=expander.get_pin(0)
blue_led.switch_to_output(value=False)
global humidity
def watering(humidity_sp, duration, periodicity):
	global user_interrupt
    user_interrupt = 0
    blue_led.value=False
	while (humidity<humidity_sp) and (user_interrupt == 0):
		blue_led.value=True
		time.sleep(duration)
		blue_led.value=False
		time.sleep(periodicity)
		if (user_interrupt) == 1 or (humidity>=humidity_sp):
               blue_led.value=False
def watering_stop():
	global user_interrupt
    user_interrupt = 1
    blue_led.value=False
while True:
	global humidity
	humidity, temperature = Adafruit_DHT.read_retry(11, 16)
