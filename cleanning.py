import RPi.GPIO as GPIO

boardPins = {7, 11, 12, 13, 15, 16, 18, 22, 29, 31, 32, 33, 35, 36, 37, 38, 40}
bcmPins = {4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27}

GPIO.setmode(GPIO.BOARD)

for pin in boardPins:
	GPIO.setup(pin, GPIO.OUT)

GPIO.cleanup()
