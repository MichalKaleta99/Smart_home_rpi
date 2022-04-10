import RPi.GPIO as GPIO
import os
import time
from gpiozero import LightSensor
import smbus
import busio
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT) #dioda PWM
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
spi.max_speed_hz=1000000
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs)
ldr_adc = AnalogIn(mcp, MCP.P2)
DEVICE     = 0x23 
POWER_DOWN = 0x00 
POWER_ON   = 0x01 
RESET      = 0x07 
CONTINUOUS_LOW_RES_MODE = 0x13
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
ONE_TIME_HIGH_RES_MODE_1 = 0x20
ONE_TIME_HIGH_RES_MODE_2 = 0x21
ONE_TIME_LOW_RES_MODE = 0x23
bus = smbus.SMBus(1)
lighting_led = GPIO.PWM(12,100) #(numer pinu, czestotliwosc wypelnienia)
lighting_led_fill = 0
lighting_percent_value = 0

def digital_lighting_value():
      data = bus.read_i2c_block_data(0x23,ONE_TIME_HIGH_RES_MODE_1)
      global digital_lighting_percent_value
      max_digital_light = 183.5
      min_digital_light = 8.498
      result=(data[1] + (256 * data[0])) / 1.2
      digital_lighting_percent_value = int(100* (min_digital_light-result)/(min_digital_light-max_digital_light))# obliczanie procentowej wartosci oswietlenia na podstawie zmierzonych czasow ladowania kondensatora, wartosc w %
      if digital_lighting_percent_value > 100:
         digital_lighting_percent_value = 100
      if digital_lighting_percent_value < 0:
         digital_lighting_percent_value = 0
      result = 0   
      return digital_lighting_percent_value     
def adc_lighting_value():
    global adc_lighting_percent_value
    min_adc_light = 5213
    max_adc_light = 39714
    measured_adc_light = ldr_adc.value
    adc_lighting_percent_value = int(100* (min_adc_light-measured_adc_light)/(min_adc_light-max_adc_light))
    if adc_lighting_percent_value > 100:
         adc_lighting_percent_value = 100
      if adc_lighting_percent_value < 0:
         adc_lighting_percent_value = 0
      measured_adc_light = 0 
      return adc_lighting_percent_value
def capacitor_lighting_value():
    impulse_counter = 0 
    capacitor_charging_seconds = 0
    global lighting_percent_value
    max_light = 0.016769 # minimalny czas na naladowanie kondensatora (oznacza maksymalne mozliwe oswietlenie)
    min_light = 0.27627 # maksymalny czas na naladowanie kondensatora (oznacza minimalne mozliwe oswietlenie)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.LOW)
    time.sleep(1) 
    GPIO.setup(26, GPIO.IN) 
    while GPIO.input(26) == GPIO.LOW:
        impulse_counter += 1     
    capacitor_charging_seconds = impulse_counter/1000000
    lighting_percent_value = int(100* (min_light-capacitor_charging_seconds)/(min_light-max_light))# obliczanie procentowej wartosci oswietlenia na podstawie zmierzonych czasow ladowania kondensatora, wartosc w %
    if lighting_percent_value > 100:
        lighting_percent_value = 100
    if lighting_percent_value < 0:
        lighting_percent_value = 0
    impulse_counter = 0
    return lighting_percent_value
def main():    
    pass
def led_pwm(action):
    global user_interrupt
    user_interrupt = 0
    lighting_led.stop()
    if action == 'ldr_capacitor':
        while user_interrupt == 0:
            lighting_led_fill = capacitor_lighting_value()
            lighting_led.start(100 - lighting_led_fill)
            if user_interrupt == 1:
                lighting_led.stop()
                lighting_led_fill = 0    
    if action == 'digital_sensor':
        while user_interrupt == 0:
            lighting_led_fill = digital_lighting_value()
            lighting_led.start(100 - lighting_led_fill)
            time.sleep(0.5)
            if user_interrupt == 1:
                lighting_led.stop()
                lighting_led_fill = 0 
    if action == 'ldr_adc':
        while user_interrupt == 0:
            lighting_led_fill = adc_lighting_value()
            lighting_led.start(100 - lighting_led_fill)
            time.sleep(0.5)
            if user_interrupt == 1:
                lighting_led.stop()
                lighting_led_fill = 0            
def led_stop():
    global user_interrupt
    user_interrupt = 1
    lighting_led.stop()
    lighting_led_fill = 0
if __name__ == '__main__':
    main()
