import configparser

def getSensorsDict():
    """
        Get the list of sensors in sensors.ini file, and return all information about all sensors 
        Including actual meassurement and math calc to get the real result 
    """
    sensors = configparser.ConfigParser()
    sensors.read("sensors.ini")
    sensorList = {}
    for gpio in sensors.sections():
        sensor = sensors[gpio]
        data = {
            'name'      :     sensor.get('name', 'no_name'),
            'math'      :     sensor.get('math', 'x'),
            'unit'      :     sensor.get('unit', 'undefined')
        }
        x = getSensorData(gpio)
        data['meassure'] = eval(data['math'])
        sensorList[gpio] = data
    return sensorList

def getSensorData(gpio):
    """
        Read the information in GPIO port of raspberry.
        TODO: implement
    """
    return 0