#coding=utf-8
import RPi.GPIO as GPIO
import time

LAND = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LAND, GPIO.IN)

try:
	while True:
		print(GPIO.input(LAND))
		time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()
	print("종료")
