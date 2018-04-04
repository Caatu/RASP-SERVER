import RPi.GPIO as GPIO
import time
import configparser

def activeAlert(alert):
    if(alert['type'] == 'buzzerAlert'):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(alert['gpio'], GPIO.IN)
        GPIO.setup(alert['gpio'], GPIO.OUT)

        period = 1.0 / 3951 		 
        delayValue = period / 2		 
        numCycles = int((0.800 / 12) * frequency)	 
        
        for i in range(numCycles):		
            GPIO.output(buzzer_pin, True)	
            time.sleep(delayValue)		
            GPIO.output(buzzer_pin, False)	
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
        alert = alerts[name]
        alertList.append()
    return alertList

def compareAlerts(sensorMeassurements):
    for alert in getAlertsList():
        for meassurement in sensorMeassurements:
            if alert['sensorName'] == meassurement['name']:
                # Check if the meassurement of the sensor is in the range of the alert
                if(meassurement['meassurement'] < alert['min'] and 
                    meassurement['meassurement'] > alert['max']):
                    activeAlert(alert)