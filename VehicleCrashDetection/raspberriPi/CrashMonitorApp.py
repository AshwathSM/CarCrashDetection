'''
Created on Dec 6, 2018

@author: ashwath

This is the main application which runs on the constrained device.
This calls the Sensor adaptor (checks the sensor for any crash and calls the coap client to send the
crash information). Also it starts the CoapServer to wait for any notification from the cloud
'''

from time import sleep
import SensorAdaptor
import CoapServerApp

#Create the instance of sensor adaptor and coapServer
sensorAdaptor = SensorAdaptor.SensorAdaptor()
waitfornote = CoapServerApp.WaitForNote()

#start both the adaptor to check continuously for any crash and then start the server 
# to listen to any notifications from the cloud in case of the crash
sensorAdaptor.run()
print('THIS IS TO TEST')
waitfornote.waitForNotify()

#wait time
while(True):
    sleep(5)
    pass
