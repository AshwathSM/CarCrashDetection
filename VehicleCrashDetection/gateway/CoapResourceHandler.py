'''
Created on Dec 6, 2018

@author: ashwath

This handler class handles all the requests sent to the server by the clients
extends the Resource of the type coapthon.resources.resource
Reference: https://github.com/Tanganelli/CoAPthon 
'''
from coapthon.resources.resource import Resource
import gateway.EmergencyPublish 

class TestCoapResource(Resource):
    
    def __init__(self, name= "TestCoapResource", coap_server = None):
        
        
        '''
        Constructor
        creates a test resource with the name "TestResource" with visibility, observable and allow_children set to true
        '''
        super(TestCoapResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        
        #define the payload, resource type, content type and interface type
        self.payload = "Test Coap Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        
    
    def render_GET(self, request):
        
        '''
        Not used in this project
        handles the get request from the clients
        for test purposes, i am returning the content of a text file stored in local directory
        '''
        
        print("successfully retrieved this message from TestCoapResource. Payload: "+ str(self.payload))
        
        file_handler = open("/home/ashwath/Downloads/testFile", "r")    
        
        self.payload = file_handler.read()   
        
        file_handler.close()     

        return self
    
    def render_POST(self, request):
        
        '''
        This handles the requests from the client to post (create new transactions)
        
        In this project, when the data from the constrained device is arrived, this function calls 
        the MQTT publish broker to post an emergency notification to cloud
        '''
        
        #create a test resource
        res = TestCoapResource()
        
        #open the file to write and which returns the file handler, for DEBUGGING
        file_handler = open("/home/ashwath/Downloads/testFile", "w")        
        
        #payload is taken from the POST request
        res.payload = request.payload
        
        #use filehandler to write the file with received the payload,
        # close the file handler after writing
        file_handler.write(request.payload)

        file_handler.close()
        
        #Call emergency publish (MQTT publish client) to send the message (crash detected alert) to the cloud
        gateway.EmergencyPublish.emrgencyPub(1)
                
        return res
    
    def render_DELETE(self, request):
        '''
        Not used. Handles the delete requests from the clients
        for testing, i am deleting the content of a text file in the local directory
        ''' 
        
        self.payload = request.payload
        
        file_handler = open("/home/ashwath/Downloads/testFile", "w")
        
#         file_handler.write(self.payload)
        
        file_handler.close()
        
        return True
    
    def render_PUT(self, request):
        '''
        not used. Handles the update request from the client
        gets the payload from the client and updates the resource with it
        '''
        
        self.payload = request.payload
        
        file_handler = open("/home/ashwath/Downloads/testFile", "a")
        
        file_handler.write(self.payload)
        
        file_handler.close()
        
        return self
    
        