import configparser
from gpiozero import CPUTemperature

def getSensorsList():
    """
        Get the list of sensors in sensors.ini file, and return all information about all sensors 
        Including actual meassurement and math calc to get the real result 
    """
    sensors = configparser.ConfigParser()
    sensors.read("sensors.ini")
    sensorList = []
    for name in sensors.sections():
        sensor = sensors[name]
        data = getSensorData(name, sensor)
        sensorList.append(data)
    return sensorList

def getSensorData(sensor):
    """
        Read the information in GPIO port of raspberry.
        TODO: implement
    """
    data = {
        'name': name,
    }
    sensorType = sensor.get('type', '')
    if(sensorType == 'cpuTemperatura'):
        data['meassurement'] = cpu.temperature

    return data