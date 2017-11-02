import RPi.GPIO as GPIO
import time
from DHT11_Python.dht11 import DHT11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

try:
	while True:
		instance = DHT11(pin = 8)
		result = instance.read()

		if result.is_valid():
			print("Temperature: %d C" % result.temperature)
			print("Humidity: %d %%" % result.humidity)
			time.sleep(0.5)
		else:
			print("Error: %d" % result.error_code)

except KeyboardInterrupt:
	GPIO.cleanup()
