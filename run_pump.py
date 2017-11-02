#coding:utf-8
import RPi.GPIO as GPIO
import time

pump = None

PUMP = 40


GPIO.setmode(GPIO.BOARD)
GPIO.setup(PUMP, GPIO.OUT)

try:
	while True:
		GPIO.output(PUMP, GPIO.HIGH)
		time.sleep(5)
except KeyboardInterrupt:
	GPIO.cleanup()
	print("종료")
