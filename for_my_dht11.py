import RPi.GPIO as GPIO
from flask import Flask

app = Flask(__name__)

#pin set
PIN = 8
SENSOR = 'DHT11'

#GPIO set
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
GPIO.cleanup()

def read(pin):
	if pin is None or int(pin) < 0 or int(pin) > 28:
		raise ValueError('Not valid GPIO Pin. Use valid GPIO Pin in 0-27')
	

#ajax
@app.route('/getTempHumi')
def getTempHumi():
	data = "a"
	
	return data
