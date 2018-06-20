#!/usr/bin/python3
import json, time, os, sys
import paho.mqtt.client as mqtt
import getpass

from dotenv import load_dotenv
from callbacks import *
from getsensors import *
from alerts import *
from time import sleep

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
    #try:
    client.connect(broker,port=port)
    #except:
    #    print("Connection failed")
    #    client.bad_connection_flag = True
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
        Finish the loop of callbacks from paho-mqtt and exit the program
    """
    client.disconnect()
    client.loop_stop()
    sys.exit()


def generateObjetc(measurement, unit):
    """
        Generate an python dict and serialize to json object
    """
    data = {
        'measurement': measurement,
        'unit': unit
    }
    return json.dumps(data)

def getMAC():
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/%s/address' % getEthName()).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]

def getEthName():
  # Get name of the Ethernet interface
  try:
    for root,dirs,files in os.walk('/sys/class/net'):
      for dir in dirs:
        if dir[:3]=='enx' or dir[:3]=='eth':
          interface=dir
  except:
    interface="None"
  return interface

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
    envpath = os.getcwd()+"/.env"
    load_dotenv(verbose=True,dotenv_path = envpath)
    username = os.getenv("BROKER-USERNAME")
    password = os.getenv("BROKER-PASSWORD")
    client_id = getpass.getuser()
    broker = os.getenv("BROKER-IP")
    port = int(os.getenv("BROKER-PORT"))
    # Initializing components
    initializeConnection(username,password,client_id,broker,port)
    # Subscribe to receive all messages.... Tests...
    subscribeTopic('/gustavoguerino2@gmail.com/#')
    # Sending data
    error = False
    while(not error):
        sensorList = getSensorsList() 
        for sensor in sensorList:
            topic = "/gustavoguerino2@gmail.com/{}/{}/{}/".format(getMAC(), sensor['name'], sensor['meassurementType'])
            data = generateObjetc(sensor['meassurement'] ,sensor['meassurementUnit'])
            sendData(topic,data)
            # Check alerts
            compareAlerts(sensorList)
            # Sleep 1 seconds and send data again
        time.sleep(3)

if __name__ == "__main__":
    # execute only if run as a script
    main()
