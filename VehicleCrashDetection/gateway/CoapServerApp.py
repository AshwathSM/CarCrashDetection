'''
Created on Dec 6, 2018

@author: ashwath
'''

from gateway.CoapServerConnector import CoapServerConnector
import gateway.EmergencySubscribe 

def main():
    ipAddr       = "0.0.0.0"
    port         = 5683
    useMulticast = False
    coapServer   = None
        
    try:
        gateway.EmergencySubscribe.notifyDevice()
        coapServer = CoapServerConnector(ipAddr, port, useMulticast)
        try:
            coapServer.listen(10)
            print("Created CoAP server ref: " + str(coapServer))
        except Exception:
            print("Failed to create CoAP server reference bound to host: " + ipAddr)
            pass
    except KeyboardInterrupt:
        print("CoAP server shutting down due to keyboard interrupt...")
    
    if coapServer:
        coapServer.close()
    
    print("CoAP server app exiting.")
                    



if __name__ == '__main__':
    main()


