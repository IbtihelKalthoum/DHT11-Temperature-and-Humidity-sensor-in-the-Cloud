#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import RPi.GPIO as GPIO
import os
from time import sleep
import Adafruit_DHT
import urllib3
import urllib.request
import pyrebase 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#config firebase
config = {
 "apiKey": "AIzaSyAYzRsReHqHuuVE-qx6vbZrhbI70R8w8pA",
  "authDomain": "tp3-iot-f7cdc.firebaseapp.com",
  "databaseURL": "https://tp3-iot-f7cdc-default-rtdb.firebaseio.com",
  "storageBucket": "tp3-iot-f7cdc.appspot.com",
  "projectId": "tp3-iot-f7cdc",
}
#config Thingspeak
#Setup our API and delay
myAPI = "XGEE4WU0VPS44A9T"
myDelay = 10 #how many seconds between posting data
# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT11
pin = 17
# Try to grab a sensor reading. Use the read_retry method which will 
#retry up to 15 times to get a sensor reading (waiting 10 seconds between
#each retry).
def getSensorData():
 humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
 
 return (str(humidity), str(temperature))
#initialisation de la connection à Firebase 
firebase = pyrebase.initialize_app(config) 
# main() function
def main():
 
 print('starting...')
 
 # connection à thingspeak
 baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
 print (baseURL)
 
 while True:
     
  
     try:
         
         
         humid, temp = getSensorData()
         data = {"temp": temp, "humidity": humid}
 
 #connexion au firebase et envoie des données 
         db = firebase.database()
 
         results = db.child("users").push(data)
 
 #envoie des données vers thingspeak
         f = urllib.request.urlopen(baseURL +"&field1=%s&field2=%s"%(temp, humid))
         print(f.read())
         print(temp + " " + humid)
         f.close()
 
         sleep(int(myDelay))
 
     except:
       print('exiting.')
     break
 
# call main
if __name__=='__main__':
 main()

