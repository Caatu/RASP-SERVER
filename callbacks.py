def on_connect(client, userdata, flags, rc):
    """
        Callback funcition to control the network loop
        Values to rc:
            0: Connection successful
            1: Connection refused – incorrect protocol version
            2: Connection refused – invalid client identifier
            3: Connection refused – server unavailable
            4: Connection refused – bad username or password
            5: Connection refused – not authorised
    """
    if(rc == 0):
        client.connected_flag = True
        print("Connection OK")
    else:
        client.bad_connection_flag = True
        print("Bad connection Returned code=",rc)


def on_log(client, userdata, level, buf):
    print("Log: ",buf)

def on_message(client, userdata, message):
    print("Message received " ,str(message.payload.decode("utf-8")))
    print("Message topic=",message.topic)
    print("Message qos=",message.qos)
    print("Message retain flag=",message.retain)
