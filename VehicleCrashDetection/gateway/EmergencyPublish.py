'''
Created on Dec 4, 2018

@author: ashwath

MQTT publish client
Runs on the gateway device
Sends the notification to cloud  
Uses  secure connection (SSL)

implements paho mqtt client
'''


import paho.mqtt.client as mqttClient
from gateway.SmtpClientConnector import SmtpClientConnector
from gateway import ConfigConst
from gateway import ConfigUtil
import time
import json
import ssl


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


def on_publish(client, userdata, result):
    '''
    Called when the publish to the broker is successful
    '''
    #Instantiate SmtpClient class and send the mail to the user
    connector = SmtpClientConnector() 
    
    '''send a mail to the driver to inform him that the emergency is notified'''   
    connector.publishMessage("Crash Details sent to the emergency")
    
    '''display on console that the message is published--DEBUG'''
    print("Published!")


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
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        
        #callback to paho mqtt client on_connect method
        mqtt_client.on_connect = on_connect
        
        #callback to paho mqtt client on_publish method
        mqtt_client.on_publish = on_publish
        
        #add ssl certificate from the Ubidots and specify the versions of the TLS protocol
        mqtt_client.tls_set(ca_certs=cert, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        
        #secure connection
        mqtt_client.tls_insecure_set(False)
        
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


def publish(mqtt_client, topic, payload):
    '''
    This method tries to publish (send data) to the broker, i.e "things.ubidots.com" in this case
    '''
    try:
        
        #publish the payload specified on the specified topic
        mqtt_client.publish(topic, payload)

    except Exception as e:
        #raise exception in case of failure to publish
        print("[ERROR] Could not publish data, error: {}".format(e))


def emrgencyPub(valtopub):
    
    '''
    this method creates MQTT client, establishes the connection by calling connect function
    creates a pyload and topic to send and then publishes to the cloud  by calling
    publish function
    '''
    
    
    '''Read all the user specific data from the properties file
    (mqtt broker IP, TLS port number, authentication to be attached with the client to 
    establish connection, topic (device edited in the ubidots) on the cloud to subscribe to) '''    
    #load configuration file using ConfigUtil
    config=ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
    config.loadConfig()
    
    BROKER_ENDPOINT = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.HOST_KEY)
    TLS_PORT = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.PORT_KEY)    
    MQTT_USERNAME = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.USER_NAME_TOKEN_KEY)
    MQTT_PASSWORD = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.USER_AUTH_TOKEN_KEY)
    TLS_CERT_PATH = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.CERT_PATH)
    TOPIC = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.PUB_TOPIC)
    DEVICE_LABEL = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.PUB_DEVICE)
    
    
    print('from gateway Mqtt publish to cloud')
    
    #create the payload in json format 
    payload = json.dumps({"value": valtopub })
    
    #create the topic using the application name and device name on 
    #the ubidots cloud read from properties file
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)
    
    #test by printing the payload
    print(type(payload))
    
    #create the client
    mqtt_client = mqttClient.Client()

    #connection creation if there's no previous one
    if not connect(mqtt_client, MQTT_USERNAME,
                   MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT, TLS_CERT_PATH):
        return False
    i=0
    
    #attempt 4 times to publish 
    while(i<4):
        publish(mqtt_client, topic, payload)
        i+=1
        time.sleep(10)
    return True


