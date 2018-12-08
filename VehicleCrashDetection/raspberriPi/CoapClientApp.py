'''
Created on Dec 4, 2018

@author: ashwath

This module instantiates the CoapClientConnector class and sends the 
information to the gateway in case of vehicle crash 

'''

# import psutil
from time import sleep
import CoapClientConnector


def startApp():


    #Instantiate the thread class (create the thread)
    coapClient = CoapClientConnector.CoapClientConnector()

    #a topic to subscribe to and also create a payload to send to gateway
    resource = "temp"
    payload = "from coapClient in raspberri to COap server in gateway"


    #Post the crash details to the gateway device
    coapClient.handlePostTest(resource, payload)
    
    #Test Code to get back the posted payload
    coapClient.handleGetTest(resource)
    
 
