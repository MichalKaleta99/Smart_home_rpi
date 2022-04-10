import RPi.GPIO as GPIO
import os
import time
import sqlite3
from dateutil import parser
from gpiozero import LightSensor
from flask import Flask, render_template, request, redirect, flash
from lighting_control import led_pwm, led_stop, digital_lighting_value, capacitor_lighting_value, adc_lighting_value
from temperature_control import fan_manual, temp_pv_function, heater_manual, temp_control_automatic, temp_control_stop
from watering_control import watering, watering_stop
from blinds_control import blinds
from gate_control import gate
from doors_control_from_site import doors_control
from alarm_control import pin_alarm
app = Flask(__name__)
import datetime
app.secret_key="123"

@app.route("/", methods=['POST', 'GET'])
def index_html():
    if request.method=='POST':
        name = request.form['name']
        password = request.form['password']
        con = sqlite3.connect("mydb.db")   
        c = con.cursor()
        statement=("select * from user where name=? and password=?")
        c.execute(statement, (name, password))
        if c.fetchone():
            return redirect('/templates/home')
        else:  
            now = datetime.datetime.now()
            timeString = now.strftime("%Y-%m-%d %H:%M") 
            c.execute ("INSERT INTO alarmy (data, alert) VALUES (?, ?)",(timeString, 'Wykryto błędne dane logowania'))
            con.commit()
            flash('Błędny login lub hasło!')
            return render_template('index.html')      
    return render_template('index.html')
@app.route("/templates/lighting/", methods=['POST', 'GET'])
def lighting_html():    
    if request.method == 'POST':
        if "ldr_capacitor" in request.form:  
                led_pwm('ldr_capacitor')
        elif "digital_sensor" in request.form:
                led_pwm('digital_sensor')
        elif "lighting_stop" in request.form:
                led_stop()
    templateData = {
        'capacitor_percentage_value' : capacitor_lighting_value(),
        'digital_percentage_value': digital_lighting_value(),
        'adc_percentage_value' : adc_lighting_value()
        }
    return render_template("lighting.html", **templateData)
@app.route("/templates/door/", methods=['POST', 'GET'])
def door():   
    if request.method == 'POST':
        if "doors_off" in request.form:
            doors_control('off')            
    return render_template("door.html")
@app.route("/templates/door_alert/", methods=['POST', 'GET'])
def door_alert():
    pin_alarm()
    if request.method == 'POST':
        if "doors_off" in request.form:
            doors_control('off')           
    return render_template("door.html")
@app.route("/templates/alerts/")
def alerts():
    con = sqlite3.connect("mydb.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from alarmy order by data desc")  
    rows = cur.fetchall()
    return render_template("alerts.html",rows = rows)  
@app.route("/templates/temp/", methods=['POST', 'GET'])
def temp_html():
    if request.method == 'POST':
        if "fan_automatic" in request.form:  
            temp_sp = request.form['temp_sp']
            temp_sp = float(temp_sp)
            temp_control_automatic(temp_sp)
        elif "fan_manual" in request.form:
            rpm = request.form['rpm']
            fan_manual(rpm)
        elif "heater_manual" in request.form:
            heat_level = request.form['heat_level']
            heater_manual(heat_level)
        elif "temp_control_stop" in request.form:
            temp_control_stop()   
    templateData = {
        'fan_fdbck_percentage' : fan_fdbck()
        }   
    return render_template('temp.html', **templateData)
@app.route("/templates/blinds/", methods=['POST', 'GET'])
def blinds_html():
    if request.method == 'POST':
        if "blinds_on" in request.form:  
            blinds('on')
        elif "blinds_off" in request.form:
            blinds('off') 
        elif "blinds_stop" in request.form:
            blinds('stop')   
    return render_template('blinds.html')
@app.route("/templates/gate/", methods=['POST', 'GET'])
def gate_html():
    if request.method == 'POST':
        if "gate_on" in request.form:  
            gate('on')
        elif "gate_off" in request.form:
            gate('off')
        elif "gate_stop" in request.form:
            gate('stop') 
    return render_template('gate.html')
@app.route("/templates/main/")
def main_redirect_html():
        return render_template('main.html')
@app.route("/templates/home/")
def home_html():
    with sqlite3.connect("mydb.db") as con:
         c = con.cursor()        
         c.execute('SELECT date, temp FROM tmp')
         data = c.fetchall()
         dates = []
         values = []    
         for row in data:
             dates.append(parser.parse(row[0]))
             values.append(row[1])
                   
             labels = [row[0] for row in data]
             values = [row[1] for row in data]

    templateData = {
        'capacitor_percentage_value' : capacitor_lighting_value(),
        'digital_percentage_value': digital_lighting_value(),
        'adc_percentage_value' : adc_lighting_value(),
        'temp_pv' : temp_pv_function()
        }
    return render_template('home.html', labels = labels, values = values, **templateData)
@app.route("/templates/watering/")
def watering():
     if request.method == 'POST':
        if "watering" in request.form:  
            humidity = request.form['temp_sp']
            duration = request.form['duration']
            periodicity = request.form['periodicity']
            watering(humidity_sp, duration, periodicity)
        elif "watering_stop" in request.form:
            watering_stop()      
    return render_template('watering.html')
@app.route("/templates/door_on/", methods=['POST', 'GET'])
def door_on():
    if request.method == 'POST':
        if "doors_on" in request.form:  
            doors_control('on')
        elif "doors_off" in request.form:
            doors_control('off') 
    return render_template('door_on.html')

if __name__ == '__main__':
    app.run(debug=True, port=8202, host='192.168.0.18')



    


                         