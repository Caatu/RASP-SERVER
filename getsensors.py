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
        sensorList.extend(data)
    return sensorList

def getSensorData(name, sensor):
    """
        Read the information in GPIO port of raspberry.
        
        All sensortypes need have type unit and the result of meassurement
    """
    data = {
        'name': name,
    }
    sensorType = sensor.get('type', '')
    if(sensorType == 'cpuTemperatura'):
        cpu = CPUTemperature()
        data['meassurement'] = cpu.temperature
        data['meassurementType'] = 'temperatura'
        data['meassurementUnit'] = 'Celsius'
    elif(sensorType == 'dht22Temperatura'):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensor.get('gpio'))
        data['meassurement'] = temperature
        data['meassurementType'] = 'temperatura'
        data['meassurementUnit'] = 'Celsius'
    elif(sensorType == 'dht22Umidade'):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, sensor.get('gpio'))
        data['meassurement'] = humidity
        data['meassurementType'] = 'umidade'
        data['meassurementUnit'] = 'Porcentagem'

    return data