[![Build Status](https://www.travis-ci.com/codetrav/3308project.svg?branch=master)](https://www.travis-ci.com/codetrav/3308project)
# smartOBD

Overview
========

The SmartOBD is an open-source, customizable, and accessible OBD scanner and user interface, targeted towards individuals who aren't mechanics but want an easy way of reading their car's on board diagnostics (OBD) system. It is comprised of the physical OBD scanner as well as a supplementary user interface that presents over 200 pieces of data from the OBD in an understandable manner for the user.

The associative website is comprised of three parts: a home dashboard, a data log of previous OBD readings, and a live log page that displays current OBD readings. The user can create an account with multiple cars so that they can view the dashboard, history log, and live log for each of their cars. The dashboard presents the most important information to the user, including various temperatures and pressures, scanning history, and miles traveled since previously scanned.

Ultimately, the SmartOBD helps car owners become more informed about the condition of their vehicles without constantly having to visit a mechanic. It provides a wealth of information in a readable manner, including the status of the malfunction indicator light, diagnostic trouble codes, inspection and maintenance information, freeze frames, VIN, hundreds of real-time metrics. For users who are more knowledgeable about cars, it provides them the opportunity to utilize that it is open-source and customize which commands they'd like to see and clear codes.

How to Run
==========
Take your SmartOBD and USB-to-OBD-II adapter, and plug the USB into your computer and the OBD-II adapter into your car's OBD port (it's usually located under the dashboard, beneath the steering wheel).

Open up the [user interface](<https://smart-obd.herokuapp.com/>), create an account, add a vehicle

Github Organization/Structure:
===
Not sure how much in depth we need to go

## Development files

 Files used in development stages, deprecated methods

## Smart OBD

 ### Nodejs

  Contains all files for node server to be deployed on heroku

## Dynamic_commands

 ### Docs

  Contains documentation for executable

 ### Tests

  Unittesting

 ### Executable

  Compile files for executable

 ### smartOBD

  Python package to be used in main.py

# How to Build, Run, and Test Code: 

Run.sh - 

Takes arguments to build an executable, run the raw source code, compile sphinx docs for the executable, and run pytest on the source code. Call run.sh in root folder to see all options

To access application, go to smart-obd.herokuapp.com

 _May also need to go to wiwa-hasura.herokuapp.com/console in order to wake up the database_

# Dependences:

`obd == 0.7.1`

`progressbar == 2.5`

`psycopg2-binary == 2.8.4`

`postgreSQL == 12.1`