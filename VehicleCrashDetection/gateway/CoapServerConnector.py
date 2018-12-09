'''
Created on Dec 5, 2018

@author: ashwath

Create a server connector by extending CoAP class of coapthon
 Refer: https://github.com/Tanganelli/CoAPthon 
'''
from coapthon.server.coap import CoAP
from gateway import ConfigUtil
from gateway import ConfigConst

from gateway.CoapResourceHandler import TestCoapResource

class CoapServerConnector(CoAP):
    
    config=None
    
    def __init__(self, ipAddr = "0.0.0.0", port = 5683, multicast = False):
        
        #Print configuration data
        print('Configuration data...\n' + str(self.config))
        
        #initialize the coap server with the default port(5683) and ip address (any outside IPv4)
        #initialize resources
        CoAP.__init__(self, (ipAddr, port), multicast)
        if port >= 1024:
            self.port = port
        else:
            self.port = 5683
        self.ipAddr   = ipAddr
        self.useMulticast = multicast
        self.initResources()
    
    '''
    Test
    '''
    def TestCoapResource(self):
        print("sadfas")
        
        
    '''
    initialize the server with the handler whenever the new request arrives on the topic 'temp' 
    '''
    def initResources(self):
        self.add_resource('temp', TestCoapResource())
        print("CoAP server initialized. Binding: " + self.ipAddr + ":" + str(self.port))
        print(self.root.dump())
        
        

        
    

