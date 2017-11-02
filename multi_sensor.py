from flask import Flask, render_template
#from Adafruit_Python_DHT.Adafruit_DHT import common
import RPi.GPIO as GPIO
import time

#flask
app = Flask(__name__)

#pin
dht_pin = 8
led_pin = 10
sound_pin = 12

#GPIO setting
GPIO.setmode(GPIO.BOARD)
GPIO.setup(dht_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(sound_pin, GPIO.IN)


@app.route('/')
def index():
	return render_template('sensors_index.html')

@app.route('/LED/<switch>')
def led_controll(switch):
	switch_on = array(
		'ON',
		'on',
		'1'
	)
	switch_off = array(
		'OFF',
		'off',
		'0'
	)

	if switch in switch_on:
		GPIO.output(led_pin, GPIO.HIGH)
	elif switch in switch_off:
		GPIO.output(led_pin, GPIO.LOW)

@app.route('/SOUND')
def _sound():
	sound = GPIO.input(sound_pin)
	return sound

@app.route('/DHT')
def _dht():
	dht = GPIO.output(dht_pin)
	return dht


#flask operate
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8888)

GPIO.cleanup()
