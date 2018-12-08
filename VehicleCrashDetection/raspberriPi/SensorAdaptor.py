'''
Created on Dec 6, 2018

@author: ashwath

Sensor adaptor will continuously get sensor data from the IR sensor
in case of any crash, it starts the CoAP client application to send
the crash information to the gateway device
'''

import RPi.GPIO as IO
from time import sleep
import CoapClientApp

class SensorAdaptor():

    #set-up to read the GPIO pins, set up pin no. 18 as the input pin
    IO.setwarnings(False)
    IO.setmode(IO.BCM)
    IO.setup(18,IO.IN) 
   

  #  def __init__(self):
            
        
    
    def run(self):
        while 1:    
            #if the input at pin 18 in high (any object in from of the IR sensor)
            if(IO.input(18)==True):
                print("object")
                # there is an object (crash) and so start the coap client and come out of the loop
                CoapClientApp.startApp()                
                break 
            #`:else:
                # print("no object")
        








