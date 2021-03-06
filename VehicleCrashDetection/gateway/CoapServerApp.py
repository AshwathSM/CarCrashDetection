'''
Created on Dec 6, 2018

@author: ashwath
Instantiates the CoapServerConnector
This server waits for any information from the coap client of constrained device 
and sends the data to the cloud via MQTT publish client
'''

from gateway.CoapServerConnector import CoapServerConnector
import gateway.EmergencySubscribe 

def main():
    '''
    application main, it starts the gateway device applications
    '''
    
    '''
    ip address from which the request can arrive (from any IP)
    the default port to which the request should arrive
    no multicast
    '''
    ipAddr       = "0.0.0.0"
    port         = 5683
    useMulticast = False
    coapServer   = None
        
    try:
        #Start the MQTT subscribe client to listen to any message from the cloud
        gateway.EmergencySubscribe.notifyDevice()
        
        #instantiate the coapServerConnector with the default details
        coapServer = CoapServerConnector(ipAddr, port, useMulticast)
        
        try:
            #listen for requests, print the log
            coapServer.listen(10)
            print("Created CoAP server ref: " + str(coapServer))
        except Exception:
            #raise an exception in case of failure to create a server
            print("Failed to create CoAP server reference bound to host: " + ipAddr)
            pass
        
    except KeyboardInterrupt:
        #come out of listening state when interrupted from keyboard (manual interrupt from user)
        print("CoAP server shutting down due to keyboard interrupt...")
    
    if coapServer:
        #in case of any previous servers, close them
        coapServer.close()
    
    print("CoAP server app exiting.")
                    



if __name__ == '__main__':
    main()


