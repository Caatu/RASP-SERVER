import RPi.GPIO as GPIO
import time
import configparser

def activeAlert(alert):
    if(alert['type'] == 'buzzerAlert'):
        port = int(alert['gpio'])
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(port, GPIO.IN)
        GPIO.setup(port, GPIO.OUT)
        period = 1.0 / 3500		 
        delayValue = period / 2		 
        numCycles = int((0.800 / 12) * 3500)	 
        
        for i in range(numCycles):		
            GPIO.output(port, True)	
            time.sleep(delayValue)		
            GPIO.output(port, False)	
            time.sleep(delayValue)

def getAlertsList():
    """
        Get the list of alerts in outputs.ini file, and return all information about all alerts 
        Including gpio port, name of sensor, type and range of value
    """
    alerts = configparser.ConfigParser()
    alerts.read("outputs.ini")
    alertsList = []
    for name in alerts.sections():
        alertsList.append(alerts[name])
    return alertsList

def compareAlerts(sensorMeassurements):
    for alert in getAlertsList():
        for meassurement in sensorMeassurements:
            if alert['sensorName'] == meassurement['name']:
                # Check if the meassurement of the sensor is in the range of the alert
                if(float(meassurement['meassurement']) < float(alert['min']) or 
                    float(meassurement['meassurement']) > float(alert['max'])):
                    activeAlert(alert)
