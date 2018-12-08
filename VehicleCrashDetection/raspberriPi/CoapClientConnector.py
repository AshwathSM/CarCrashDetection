'''
Created on Dec 4, 2018

@author: ashwath

This class is a client connector which instantiates a HelperClient of CoAPthon to
connect to the server. 
Refer: https://github.com/Tanganelli/CoAPthon 

It also implements REST handle requests

handleGetTest(), handlePutTest(), handleDeleteTest() are not used in the project
    implemented to test the modules 

'''

from coapthon.client.helperclient import HelperClient

import ConfigUtil
import ConfigConst

class CoapClientConnector(object):
    '''
    classdocs
    '''

    config = None
    serverAddr = None
    host = "localhost"
    port = 5683

    def __init__(self):
        '''
        Constructor
        
        read the config file to load the broker address, port and protocol
        '''
        self.config=ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
        self.config.loadConfig()
        
    
    def initClient(self):
        '''
        create and initialize the Mqtt Client, raise an exception in case of failure
        '''
        try:
            #create a client (HelperClient from coapthon) to connect 
            #to server at the specified address and port
            self.client = HelperClient(server=("10.0.0.70", 5683))
            
            #print details of client
            print("created coap client ref: "+ str(self.client))
            print("  coap://"+self.host+ ":" + str(self.port))
            
        except Exception:
            print("Failed to create CoAP client reference using the host: "+ self.host)
            pass
    
    def handleGetTest(self,resource):
        '''
        this method sends a get request to the server, 
        asking for details of a transaction on the specified resource
        (Not used)
        '''
        
        print("Testing GET for resource: "+ resource)
        
        #initialize the client for the connection
        self.initClient()
        
        #get the response (payload included) from the connected client
        response = self.client.get(resource)
        
        #if successful is getting the response, display the response and payload
        if response:
            print("FROM SERVER: "+response.pretty_print())
            print("PAYLOAD: "+ response.payload)
            
        else:
            print("No response for the GET request from the server using resource: "+ resource)
        
        #end the client connection after the completion of the transaction    
        self.client.stop()
        
    
    def handlePostTest(self, resource, payload):
        '''
        This method is used in the project to send the crash information to the
        gateway device
        requests to post to server resource with the payload specified, in this case
        just a new information for the gateway to process
        '''
        print("Testing POST for resource: "+ resource)
        
        #create and initialize the client before the request
        self.initClient()
        
        #send the post request and capture the response
        response = self.client.post(resource, payload)
        
        #display the response
        if response:
            print("server response to post: "+ response.pretty_print())
            
            
        else:
            print("No response for the POST request from the server for the resource: "+ resource)
        
        #end the client connection to the server and kill the client when the transaction is over
        self.client.stop()
        
    
    
    def handlePutTest(self, resource, payload):
        '''
        request to update the resource of the server with the payload specified
        '''
        print("Testing PUT for resource: "+ resource)
        
        #create and initialize the client before the request
        self.initClient()
        
        #send the request and get the response back
        response = self.client.put(resource, payload)
        
        #display the response if successful or else print the failure to get the response
        if response:
            print("server response to put: "+response.pretty_print())
            
        else:
            print("No response for the PUT request from the server for the resource: "+ resource)
        
        #clear the client connection and stop the client
        self.client.stop()
        
        
    def handleDeleteTest(self, resource):
        '''
        request to delete the resource of the server
        '''
        print("Testing DELETE for resource: "+ resource)
        
        #create and initialize the client before the request
        self.initClient()
        
        #send the request and get the response back
        response = self.client.delete(resource)
        
        #display the response if successful or else print the failure to get the response
        if response:
            print("server response to delete: "+response.pretty_print())
            
        else:
            print("No response for the DELETE request from the server for the resource: "+ resource)
            
        #clear the client connection and stop the client
        self.client.stop()
        
    

                    
            
        
