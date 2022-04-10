import RPi.GPIO as GPIO
import os
import time
import datetime
import sqlite3
import busio
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
voltage_fdbck = AnalogIn(mcp, MCP.P3)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(0, GPIO.OUT) #buzzer
def pin_alarm():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    con = sqlite3.connect("mydb.db")   
    cur = con.cursor()  
    cur.execute ("INSERT INTO alarmy (data, alert) VALUES (?, ?)",(timeString, 'Wykryto błędny PIN do drzwi'))
    con.commit()
    GPIO.output(0, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(0, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(0, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(0, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(0, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(0, GPIO.LOW)
def switch_alarm():
    GPIO.output(0, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(0, GPIO.LOW)  
def main():
    pass 
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
spi.max_speed_hz=1000000
cs = digitalio.DigitalInOut(board.CE0)
mcp = MCP.MCP3008(spi, cs)
voltage_fdbck = AnalogIn(mcp, MCP.P3)         
if __name__ == '__main__':
    while (voltage_fdbck.value<50000):
        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")
        con = sqlite3.connect("mydb.db")   
        cur = con.cursor()  
        cur.execute ("INSERT INTO alarmy (data, alert) VALUES (?, ?)",(timeString, 'Brak napięcia 12V'))
        con.commit()
        GPIO.output(0, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(0, GPIO.LOW)
        time.sleep(1)
        GPIO.output(0, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(0, GPIO.LOW)
        time.sleep(1)
        GPIO.output(0, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(0, GPIO.LOW)
        time.sleep(10)
