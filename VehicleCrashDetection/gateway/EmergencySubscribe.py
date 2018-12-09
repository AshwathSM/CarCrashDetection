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

def on_message(client, userdata, message):
    print(message.topic + " " + str(message.payload) + " OK. Payload received")
    
    fh = open("/home/ashwath/Downloads/connectedDocs/cloudTOMqttGate.txt", "w")
    fh.write("fom cloud to Mqtt gateway")
    fh.close()
    gateway.CoapClientApp.runNotifyDevice()
    
def on_subscribe(self, client, userdata, result):
    print("Subscribe Success!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port, cert):
    global connected

    if not connected:
        mqtt_client.tls_set(ca_certs=cert, certfile=None,
                            keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        mqtt_client.tls_insecure_set(False)
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_subscribe = on_subscribe

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


def subscribe(mqtt_client, topic, payload):

    try:
        mqtt_client.subscribe(topic, payload)

    except Exception as e:
        print("[ERROR] Could not subscribe data, error: {}".format(e))


def notifyDevice():
    
    config=ConfigUtil.ConfigUtil(ConfigConst.DEFAULT_CONFIG_FILE_NAME)
    config.loadConfig()
    
    BROKER_ENDPOINT = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.HOST_KEY)
    TLS_PORT = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.PORT_KEY)
    
    MQTT_USERNAME = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.USER_NAME_TOKEN_KEY)
    MQTT_PASSWORD = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.USER_AUTH_TOKEN_KEY)
    TLS_CERT_PATH = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.CERT_PATH)
    TOPIC = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.SUB_TOPIC)
    DEVICE_LABEL = config.getProperty(ConfigConst.MQTT_CLOUD_SECTION,ConfigConst.SUB_DEVICE)
    
    
    # val1 = 39
    # payload = json.dumps({"value": val1 })
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)
    # # topic = TOPIC

    mqtt_client = mqttClient.Client()

    if not connect(mqtt_client, MQTT_USERNAME,
                   MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT, TLS_CERT_PATH):
        return False

    payload = 1
    # payload is qos level here
    data = subscribe(mqtt_client, topic, payload)
    # print(data)
    # mqtt_client.subscribe(topic)
    mqtt_client.on_message = on_message
    return True


# if __name__ == '__main__':
#     while True:
#         main()
#         time.sleep(10)
