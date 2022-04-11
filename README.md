# Building automation system

Smart home - building automation system based on the Raspberry Pi minicomputer which allowed me to read various data (such as lighting intensity, temperature and humidity)
from sensors and to control the actuators such as servomechanisms (also DC motors), a fan, LED diodes and a buzzer. I also used a keyboard (which basically was just 16 
buttons) that imitated an intercom. Whole programming project was combined with self-made house mockup which photos you can see in this repo.

# Adding features

I consider that project as a fully completed physically and i do not want to add any sensors or actuators.

Programming part of the project (basically only front-end) hasn't been fully completed and I still got a lot of ideas to bring to life.

I am working with updating front-end features at my other repo (https://github.com/MichalKaleta99/Smart_home_simulation)

# Login

I am currently working at basic login system. In the smart home concept it may work as a parent-control system so it only allows selected users to be in control of some functionality (for example opening and closing the entrance door).

After running web server and navigating to default page (which is at 127.0.0.1:5000) you are asked to enter login data. For that moment you can use that:
Login : Michał
Pass : dad
or
Login: Marta
Pass: mom

# Web server

To connect back-end data with front-end data I used Python's mini framework known as Flask with using methods POST and GET.

It allows me to run a web server in my local network (defaultly - IP: 127.0.0.1 at port 5000). Ultimately in the project I don't see that as the best solution - I feel that user of the real smart home should be able to control it from all around the world.

# SQL - read and write data (SQLite)

To create functionality such as graph of the temperature (which is displayed at the main page) or login system I had to use a database. Database system in this project isnt complicated so I used simple SQLIte database. Data is stored locally in the same folder as whole project (mydb.db).

I insert a temperature (in this version of project thats random number in range of 18-26 Celsius degrees) every one hour. Inserting script should work continously.
Every time entering the main page I select last 12 positions of temperature readings and plot it at a graph. (Axis Y - temp, Axis X - date).

I also select login information from database (ultimately user should be able to edit data)

# Running project

To run a project you simply run python script called web_server.py. Then it creates a web server at 127.0.0.1:5000 and when entering - enter login (L:Michał/P:dad or L:Marta/P:mom). Then you should be able to navigate to all bookmarks visible at the screen.

Note - to insert temperature readings to database you also have to run temperature_save.py.

# Summary

I consider that project as a fully completed physically and i do not want to add any sensors or actuators.

Programming part of the project (basically only front-end) hasn't been fully completed and I still got a lot of ideas to bring to life.


