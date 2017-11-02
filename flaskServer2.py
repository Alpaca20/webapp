#/usr/lib/python2.7/dist-packages/flask
#from -> module name (directory [folder])
from flask import Flask
import RPi.GPIO as GPIO
import time
import os

#make instance
app = Flask(__name__)

LED = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(LED, GPIO.LOW)

@app.route('/')
def index():
	return 'This is the Homepage'

@app.route('/clean')
def clean():
	GPIO.cleanup()
	return 'clean'

@app.route('/test')
def test():
	return 'test'

@app.route('/profile/<username>')
def profile(username):
	return 'Your name is <h3>%s</h3>' % username

@app.route('/post/<int:post_id>')
def post(post_id):
	return 'Your ID is <h3>%d</h3>' % post_id

@app.route('/tester/<str>')
def tester(str):
	return '<script>location.href="/profile/%s"</script>' % str

@app.route('/LED/<switch>')
def led(switch):
	if(switch == 'ON'):
		GPIO.output(LED, GPIO.HIGH)
		return '!! LED ON !!\n'
	elif(switch == 'OFF'):
		GPIO.output(LED, GPIO.LOW)
		return '.. LED OFF ..\n'
	else:
		return 'Switch Command "ON" / "OFF"'

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8888)
