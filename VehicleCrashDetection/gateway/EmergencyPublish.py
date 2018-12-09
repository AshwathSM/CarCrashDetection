import paho.mqtt.client as mqttClient
from gateway.SmtpClientConnector import SmtpClientConnector
import time
import json
import ssl

'''
global variables
'''

connected = False  # Stores the connection statu
BROKER_ENDPOINT = "things.ubidots.com"
TLS_PORT = 8883  # Secure port
MQTT_USERNAME = "A1E-SN2m1TPckxGwihF3m8L8EosDhbs3US"  # Put here your Ubidots TOKEN
MQTT_PASSWORD = ""  # Leave this in blank
# TOPIC = "/v1.6/devices/homeiotgateway/tempsensor"
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "emergency/crashdetected"
TLS_CERT_PATH = "/home/ashwath/Downloads/connectedDocs/ubidots.cert"
'''
Functions to process incoming and outgoing streaming
'''

def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("[INFO] Connected to broker")
        global connected  # Use global variable
        connected = True  # Signal connection
    else:
        print("[INFO] Error, connection failed")


def on_publish(client, userdata, result):
    #Instantiate SmtpClient class and send the mail to the user
    connector = SmtpClientConnector()    
    connector.publishMessage("Crash Details sent to the emergency")
    print("Published!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.tls_set(ca_certs=TLS_CERT_PATH, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        mqtt_client.tls_insecure_set(False)
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

        attempts = 0

        while not connected and attempts < 5:  # Wait for connection
            print(connected)
            print("Attempting to connect...")
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] Could not connect to broker")
        return False

    return True


def publish(mqtt_client, topic, payload):

    try:
        mqtt_client.publish(topic, payload)

    except Exception as e:
        print("[ERROR] Could not publish data, error: {}".format(e))


def emrgencyPub(valtopub):
    
    print('from gateway Mqtt publish to cloud')
    
    payload = json.dumps({"value": valtopub })
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)
    # topic = TOPIC
    print(type(payload))
    mqtt_client = mqttClient.Client()

    if not connect(mqtt_client, MQTT_USERNAME,
                   MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT):
        return False
    i=0
    while(i<4):
        publish(mqtt_client, topic, payload)
        i+=1
        time.sleep(10)
    return True


# if __name__ == '__main__':
#     while True:
#         main()
#         time.sleep(10)
