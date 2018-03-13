import json, time, os, sys
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from callbacks import *


def initializeConnection(username, password, client_id, broker, port):
    """
        Create client object and initialize the connection with mqtt server

        More about client object:
            http://www.steves-internet-guide.com/client-objects-python-mqtt/
    """
    global client
    mqtt.Client.connected_flag = False # Control Tag (Network loop)
    mqtt.Client.bad_connection_flag = False

    client = mqtt.Client(
        client_id=client_id, 
        clean_session=False,  
    )
    client.on_connect   =   on_connect
    client.on_log       =   on_log
    client.on_message   =   on_message
    client.username_pw_set(username=username, password=password)
    print("Connecting to broker")
    try:
        client.connect(broker,port=port)
    except:
        print("Connection failed")
        client.bad_connection_flag = True
    client.loop_start()
    # Wait to connection success or error occur
    while not client.connected_flag and not client.bad_connection_flag:
        print("In wait loop")
        time.sleep(1)
    if client.bad_connection_flag:
        # When occur error in connection stop the program
        # TODO: Filter possibles errors in on_conect and print this on log file
        finish()
    print("In Main Loop")


def finish():
    """
        Finish the loop of callbacks and exit
    """
    client.disconnect()
    client.loop_stop()
    sys.exit()


def generateObjetc(name, measurement, unit):
    """
        Generate an python dict and serialize to json object
    """
    data = {
        'name': name,
        'measurement': measurement,
        'unit': unit
    }
    return json.dumps(data)


def sendData(topic, jsonObject):
    """
        Publish string to connected client
    """
    client.publish(topic,jsonObject)
    print("Data sent")

def subscribeTopic(topic):
    """
        Subscribe to an topic in connected client
    """
    client.subscribe(topic)

def main():
    """
        Start the script, loading all settings and starting connections

        UNDER DEVELOPMENT, ONLY TESTS HERE...
    """
    # Loading dotenv data
    load_dotenv()
    username = os.getenv("BROKER-USERNAME")
    password = os.getenv("BROKER-PASSWORD")
    client_id = os.getenv("USERNAME")
    broker = os.getenv("BROKER-IP")
    port = int(os.getenv("BROKER-PORT"))
    # Initializing components
    initializeConnection(username,password,client_id,broker,port)
    # Sending data TESTES APENAS
    Mensagens = 10
    print("Subscribing to topic")
    subscribeTopic('teste/topico')
    while Mensagens != 0:
        Mensagens -= 1
        time.sleep(1)
        sendData('teste/topico', generateObjetc('Temperatura','20.4','Celsius'))


if __name__ == "__main__":
    # execute only if run as a script
    main()
