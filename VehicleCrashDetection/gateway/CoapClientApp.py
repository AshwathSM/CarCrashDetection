'''
Created on Dec 4, 2018

@author: ashwath
'''

# import psutil
from time import sleep
from gateway import CoapClientConnector

def runNotifyDevice():
    #Instantiate the thread class (create the thread)
    coapClient = CoapClientConnector.CoapClientConnector()
    
    resource = "temp"
    payload = "emergency notified. this is from gateway"
    payload1 = "another line from client"
    payloadDelete = ""
    
    # coapClient.handleDeleteTest(resource, payloadDelete)
    
    coapClient.handleGetTest(resource)
    
    coapClient.handlePostTest(resource, payload)
    # 
    coapClient.handleGetTest(resource)
    # 
    # coapClient.handlePutTest(resource, payload1) 
    # 
    # coapClient.handleGetTest(resource)
    coapClient.disconnectClient()

 