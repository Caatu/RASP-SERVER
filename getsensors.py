import configparser

def getSensorsDict():
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
    print(sensorList)

def getSensorData(gpio):
    return 0