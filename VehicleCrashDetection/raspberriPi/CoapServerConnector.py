'''
Created on Dec 5, 2018

@author: ashwath

Create a server connector by extending CoAP class of coapthon
 Refer: https://github.com/Tanganelli/CoAPthon 
'''
from coapthon.server.coap import CoAP
import ConfigUtil
import ConfigConst

import CoapResourceHandler

class CoapServerConnector(CoAP):
    
    config=None
    
    def __init__(self, ipAddr = "0.0.0.0", port = 5683, multicast = False):
        
        #get the coonection details by reading the configuration files
        self.config = ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
        self.config.loadConfig()
        print('Configuration data...\n' + str(self.config))
        CoAP.__init__(self, (ipAddr, port), multicast)
        if port >= 1024:
            self.port = port
        else:
            self.port = 5683
        self.ipAddr   = ipAddr
        self.useMulticast = multicast
        self.initResources()
    
    def TestCoapResource(self):
        print("sadfas")
        
        

    def initResources(self):
        self.add_resource('temp', CoapResourceHandler.TestCoapResource())
        print("CoAP server initialized. Binding: " + self.ipAddr + ":" + str(self.port))
        print(self.root.dump())
        
        

        
    

