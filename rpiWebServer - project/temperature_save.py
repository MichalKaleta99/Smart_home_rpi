import sqlite3
import time
from time import sleep
import datetime
from temperature_control import temp_pv_function


with sqlite3.connect("mydb.db") as con:
    c = con.cursor()
         
def dynamic_data_entry():  
    unix = int(time.time())
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M'))
    temp_pv = temp_pv_function()
    c.execute("INSERT INTO tmp (date, temp) VALUES (?, ?)",(date, temp_pv))
    con.commit()
    
while True:
    dynamic_data_entry()
    time.sleep(3600)
    

    


