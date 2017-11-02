#/usr/lib/python2.7/dist-packages/flask
#from -> module name (directory [folder])
from flask import Flask
import RPi.GPIO as GPIO

#make instance
app = Flask(__name__)

LED = 8
SOUND = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(SOUND, GPIO.IN)

@app.route('/')
def index():
	return 'This is the Homepage'

@app.route('/SOUND/ON')
def sound_on():
	while(True):
		SOUND_LEVEL = GPIO.input(SOUND)
		if(SOUND_LEVEL == 0):
			led_on()
			time.sleep(1)
			return '!! SOUND DETECTED !!'
		else:
			led_off()

@app.route('/SOUND/OFF')
def sound_off():
	GPIO.cleanup()

@app.route('/LED/ON')
def led_on():
	GPIO.output(8, GPIO.HIGH)
	return '// LED ON //'

@app.route('/LED/OFF')
def led_off():
	GPIO.output(8, GPIO.LOW)
	return '.. LED OFF ..'

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8888)
