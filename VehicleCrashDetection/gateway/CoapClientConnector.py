'''
Created on Dec 4, 2018

@author: ashwath
'''

from coapthon.client.helperclient import HelperClient

from labs.common import ConfigUtil
from labs.common import ConfigConst

class CoapClientConnector(object):
    '''
    classdocs
    '''

    config = None
    serverAddr = None
    host = "192.168.43.253"
    port = 5683

    def __init__(self):
        '''
        Constructor
        '''
        self.config=ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
        self.config.loadConfig()
        
#         self.host = self.config.getProperty(ConfigConst.COAP_CLOUD_SECTION, ConfigConst.CLOUD_COAP_HOST)
#         self.port = int(self.config.getProperty(ConfigConst.COAP_CLOUD_SECTION.CLOUD_COAP_PORT))
        
#         print('\tHost: '+ self.host)
#         print('\tPort: '+ self.port)
        
#         if not self.host or self.host.isspace():
#             print("Using default host: "+ self.host)
#             
#         if self.port < 1024 or self.port>65535:
#             print("using default port: "+ self.port)
#         
#         
#         self.serverAddr = (self.host, self.port)
#         self.url = "coap://"+self.host+":"+str(self.port)
    
    def initClient(self):
        try:
            self.client = HelperClient(server=("10.0.0.219", 5683))
            print("created coap client ref: "+ str(self.client))
            print("  coap://"+self.host+ ":" + str(self.port))
            
        except Exception:
            print("Failed to create CoAP client reference using the host: "+ self.host)
            pass
    
    def handleGetTest(self,resource):
        print("Testing GET for resource: "+ resource)
        
        self.initClient()
        
        response = self.client.get(resource)
        
        if response:
            print("FROM SERVER: "+response.pretty_print())
            print("PAYLOAD: "+ response.payload)
            
        else:
            print("No response for the GET request from the server using resource: "+ resource)
            
        self.client.stop()
        
    
    def handlePostTest(self, resource, payload):
        print("Testing POST for resource: "+ resource)
        
        self.initClient()
        
        response = self.client.post(resource, payload)
        
        if response:
            print("server response to post: "+ response.pretty_print())
            
            
        else:
            print("No response for the POST request from the server for the resource: "+ resource)

        self.client.stop()
        
        
    def handlePutTest(self, resource, payload):
        print("Testing PUT for resource: "+ resource)
        
        self.initClient()
        
        response = self.client.put(resource, payload)
        
        if response:
            print("server response to put: "+response.pretty_print())
            
        else:
            print("No response for the PUT request from the server for the resource: "+ resource)

        self.client.stop()
        
        
    def handleDeleteTest(self, resource, payload):
        print("Testing DELETE for resource: "+ resource)
        
        self.initClient()
        
        response = self.client.delete(resource)
        
        if response:
            print("server response to delete: "+response.pretty_print())
            
        else:
            print("No response for the DELETE request from the server for the resource: "+ resource)

        self.client.stop()
        
    
    def pingServer(self):
        
        print("pinging server")
        
        self.initClient()
        
#         response = self.client.
               
            
    def disconnectClient(self):
        self.client.close()     
            
        