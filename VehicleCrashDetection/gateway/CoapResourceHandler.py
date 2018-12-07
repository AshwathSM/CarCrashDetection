'''
Created on Dec 6, 2018

@author: ashwath
'''
from coapthon.resources.resource import Resource
import labs.module07.EmergencyPublish 

class TestCoapResource(Resource):
    
    def __init__(self, name= "TestCoapResource", coap_server = None):
        super(TestCoapResource, self).__init__(name, coap_server, visible=True, observable=True, allow_children=True)
        
        self.payload = "Test Coap Resource"
        self.resource_type = "rt1"
        self.content_type = "text/plain"
        self.interface_type = "if1"
        
    
    def render_GET(self, request):
        print("successfully retrieved this message from TestCoapResource. Payload: "+ str(self.payload))
        
        file_handler = open("/home/ashwath/Downloads/testFile", "r")    
        
        self.payload = file_handler.read()   
        
        file_handler.close()     

        return self
    
    def render_POST(self, request):
        
        res = TestCoapResource()
#         res.location_query = request.URI_QUERY
        
        file_handler = open("/home/ashwath/Downloads/testFile", "w")        
        
        res.payload = request.payload
        
        file_handler.write(request.payload)

        file_handler.close()
        
        labs.module07.EmergencyPublish.emrgencyPub(35)
                
        return res
    
    def render_DELETE(self, request):
        
        self.payload = request.payload
        
        file_handler = open("/home/ashwath/Downloads/testFile", "w")
        
#         file_handler.write(self.payload)
        
        file_handler.close()
        
        return True
    
    def render_PUT(self, request):
        self.payload = request.payload
        
        file_handler = open("/home/ashwath/Downloads/testFile", "a")
        
        file_handler.write(self.payload)
        
        file_handler.close()
        
        return self
    
        