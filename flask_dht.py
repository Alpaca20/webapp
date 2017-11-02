#coding : UTF-8
import RPi.GPIO as GPIO
from DHT11_Python.dht11 import DHT11
from flask import Flask, render_template, jsonify

app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

@app.route('/')
def index():
	return render_template('dht11.html')

@app.route('/ajax')
def ajax():
	instance = DHT11(pin = 8)
	result = instance.read()
	
	if result.is_valid():
		temperature = str(result.temperature)
		humidity = str(result.humidity)
		return jsonify(temperature = temperature, humidity = humidity)
	else:
		return jsonify(temperature = 'error', humidity = 'error')

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8888)
