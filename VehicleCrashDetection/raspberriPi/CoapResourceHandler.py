'''
Created on Dec 6, 2018

@author: ashwath

This handler class handles all the requests sent to the server by the clients
extends the Resource of the type coapthon.resources.resource
Reference: https://github.com/Tanganelli/CoAPthon 
'''
from coapthon.resources.resource import Resource

class TestCoapResource(Resource):

    
    def __init__(self, name= "TestCoapResource", coap_server = None):
            
        '''
        constructor
        '''
        
        super(TestCoapResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        '''
        create a test resource with the name "TestResource" with visibility, observable and allow_children set to true 
        '''
        
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
        
        file_handler = open("/home/pi/ashwath_Proj/fromCloud.txt", "r")    
        
        self.payload = file_handler.read()   
        
        file_handler.close()     

        return self
    
    def render_POST(self, request):
        '''
        This handles the requests from the client to post (create new transactions)
        
        In this project, the data from the gateway device is displayed in a text 
        file for the driver to read/understand that the emergency service is on the way
        This resembles the actuator action for testing
        '''
        
        #create a test resource
        res = TestCoapResource()

        #open the file to write and return the file handler
        file_handler = open("/home/pi/ashwath_Proj/fromCloud.txt", "w")        
        
        #get the payload to write from the request (the payload from the gateway)
        res.payload = request.payload
        
        #write the data from the gateway device into the file
        file_handler.write(request.payload)

        #Close the file handler
        file_handler.close()
                
        #return the resource
        return res
    
    
    def render_DELETE(self, request):
        '''
        Not used. Handles the delete requests from the clients
        for testing, i am deleting the content of a text file in the local directory
        '''    
        self.payload = request.payload
        
        file_handler = open("/home/pi/ashwath_Proj/fromCloud.txt", "w")
        
#         file_handler.write(self.payload)
        
        file_handler.close()
        
        return True
    
    def render_PUT(self, request):
        '''
        not used. Handles the update request from the client
        gets the payload from the client and updates the resource with it
        '''
        self.payload = request.payload
        
        file_handler = open("/home/pi/ashwath_Proj/fromCloud.txt", "a")
        
        file_handler.write(self.payload)
        
        file_handler.close()
        
        return self
    
        
