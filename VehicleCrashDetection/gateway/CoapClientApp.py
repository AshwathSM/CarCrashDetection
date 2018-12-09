'''
Created on Dec 4, 2018

@author: ashwath

CoapClientApp
Runs on the gateway device
Sends the notification to constraint device
'''


from time import sleep
from gateway import CoapClientConnector

def runNotifyDevice():
    '''
    this is called by the MQTT EmergencySubscriberApp, when a message arrives from the cloud
    it will send a POST request to the coap server in constrained device 
    (send a new notification to the user)
    '''
    
    #Instantiate the thread class (create the thread)
    coapClient = CoapClientConnector.CoapClientConnector()
    
    #Create a resource name and the payload to send
    resource = "temp"
    payload = "emergency notified. this is from gateway"
   

    #send Post request to the coap server in constrained device
    coapClient.handlePostTest(resource, payload)
    
    #Get back the payload from the coap Server using the GET request 
    #code line for debugging
    coapClient.handleGetTest(resource)


 