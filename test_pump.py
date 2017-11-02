#coding:utf-8
import RPi.GPIO as GPIO
import time

pump = None

PUMP = 40


GPIO.setmode(GPIO.BOARD)
GPIO.setup(PUMP, GPIO.OUT)

'''
pump_in = GPIO.PWM(PUMP_IN, 100)

pump_out = GPIO.PWM(PUMP_OUT, 100)
pump_out.start(0)
'''
try:
	while True:
		GPIO.output(PUMP, GPIO.HIGH)
		print("켜짐")
		time.sleep(5)
		GPIO.output(PUMP, GPIO.LOW)
		print("꺼짐")
		time.sleep(5)
except KeyboardInterrupt:
	GPIO.cleanup()
	print("종료")
