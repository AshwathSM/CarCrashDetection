'''
Created on Dec 4, 2018

@author: ashwath

MQTT subscribe client
Runs on the gateway device
receives the updates from cloud  
Uses  secure connection (SSL)
implements paho mqtt client
'''

import paho.mqtt.client as mqttClient
import gateway.CoapClientApp
from gateway import ConfigConst
from gateway import ConfigUtil
import time
import json
import ssl

'''
global variables
'''

connected = False  # Stores the connection statu


def on_connect(rc):
    '''
    This method is called when the connection to broker is successful
    Implemented to display the connection success message
    '''
    if rc == 0:

        print("[INFO] Connected to broker")
        global connected  # Use global variable
        connected = True  # Signal connection
    else:
        print("[INFO] Error, connection failed")

def on_message(client, userdata, message):
    '''
    called when a message is arrived from the broker on the subscribed topic
    calls the coap client to send a notification back to the vehicle
    '''
    
    #print the arrived message and topic
    print(message.topic + " " + str(message.payload) + " OK. Payload received")
    
    #write the arrived message on a local file--DEBUG CODE
    fh = open("/home/ashwath/Downloads/connectedDocs/cloudTOMqttGate.txt", "w")
    fh.write(str(message.payload))
    fh.close()
    
    #call the Coap client to send a post request to the constrained device--notify the driver
    gateway.CoapClientApp.runNotifyDevice()
    
def on_subscribe(self, client, userdata, result):
    '''
    display the success message when subscription is established
    '''
    print("Subscribe Success!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port, cert):
    '''
    This method is used to connect to the remote broker at "things.ubidots.come" at
    port 8883
    attempts 5 times to connect, and returns true if connection is successful, else returns false
    
    '''
    
    #define a global variable to check if the connection is done
    global connected

    #start a new connection when there is no connection
    if not connected:
        
        #add the username and password for the mqtt cloud connection (cloud authentication)
        mqtt_client.tls_set(ca_certs=cert, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        
        #secure connection
        mqtt_client.tls_insecure_set(False)
        
        #add the username and password for the mqtt cloud connection (cloud authentication)
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        
        #callback to paho mqtt client on_connect method
        mqtt_client.on_connect = on_connect
        
        #callback to paho mqtt client on_subscribe method
        mqtt_client.on_subscribe = on_subscribe

        #send a connection request to the broker
        mqtt_client.connect(broker_endpoint, port=port)
        
        #wait till the connection is established (start to loop)
        mqtt_client.loop_start()

        #count the number of connection attempts
        attempts = 0

        #if the connection is not established, and number of attempts is not 5, try to connect again
        while not connected and attempts < 5:  # Wait for connection
            print(connected)
            print("Attempting to connect...")
            time.sleep(1)
            attempts += 1

    #if not connected after 5 attempts, print an error message
    if not connected:
        print("[ERROR] Could not connect to broker")
        return False

    #return true is connection is successful
    return True


def subscribe(mqtt_client, topic, payload):
    '''
    This method tries to subscribe to the broker on a specific device 
    (topic), i.e "things.ubidots.com" in this case
    '''

    try:
        mqtt_client.subscribe(topic, payload)

    except Exception as e:
        print("[ERROR] Could not subscribe data, error: {}".format(e))


def notifyDevice():
     '''
    this method creates MQTT client, establishes the connection by calling connect function
    subscribes to the topic by calling subscribe method, and receives the message from 
    the cloud  and on_message callback will be called when a message is arrived
    '''
    
    
'''
    Read all the user specific data from the properties file
    (mqtt broker IP, TLS port number, authentication to be attached with the client to 
    establish connection, topic (device edited in the ubidots) on the cloud to subscribe to)
'''    
    #load config file
    config=ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
    config.loadConfig()
    
    BROKER_ENDPOINT = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.HOST_KEY)
    TLS_PORT = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.PORT_KEY)    
    MQTT_USERNAME = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.USER_NAME_TOKEN_KEY)
    MQTT_PASSWORD = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.USER_AUTH_TOKEN_KEY)
    TLS_CERT_PATH = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.CERT_PATH)
    TOPIC = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.SUB_TOPIC)
    DEVICE_LABEL = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.SUB_DEVICE)
    
 
    #read from the topic specified in configuration file
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)
    
    #create a client
    mqtt_client = mqttClient.Client()

    #establish connection if there is no previous connection
    if not connect(mqtt_client, MQTT_USERNAME,
                   MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT, TLS_CERT_PATH):
        return False

    #specify quality of service as 1
    qos = 1
    # subscribe to the topic
    data = subscribe(mqtt_client, topic, qos)
    
    #call the function on_message when the message is arrived
    mqtt_client.on_message = on_message
    
    #returns true if subscription is successful
    return True


# if __name__ == '__main__':
#     while True:
#         main()
#         time.sleep(10)
