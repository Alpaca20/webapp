#coding:utf-8
import RPi.GPIO as GPIO
import threading, time, MySQLdb, serial
from flask import Flask, render_template, jsonify, request
import Adafruit_DHT

app = Flask(__name__)

temperature = 9999
humidity = 9999
moisture = 9999

ON = 1
OFF = 0
SUCCESS = 1
ERROR = -1
# Value 9999 also Error.
# Why 9999? Temperature to be reach -1.
# Is that Error or real temperature? So need temperature fail to be reach.

# DB connection
conn = None

# serial port
port = "/dev/ttyACM0"

# pin setting
LED = 12
DHT = 23 #BCM
DHT_MODEL = 11
FLAME = 18
PUMP = 40
MOISTURE = 38

# default temperature/humidity setting
temp = 24
humi = 40
# temperature/humidity + - error
temp_error = 3
humi_error = 5
# default moisture setting
mois = 600

# status
led_check = OFF # check LED ON or OFF
pump_check = OFF # check PUMP ON or OFF
fire_check = OFF # check FIRE Sensor ON or OFF
moisture_check = OFF # check MOISTURE Sensor ON or OFF

# GPIO setting
def init():
	global led, pump_in, pump_out, conn

#	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)
	GPIO.setup(FLAME, GPIO.IN)
	GPIO.setup(PUMP, GPIO.OUT)
#	GPIO.setup(MOISTURE, GPIO.IN)
	
	GPIO.output(PUMP, GPIO.LOW)
	
	try:
		conn = MySQLdb.connect('192.168.0.225', 'pacaAl', 'pacaLover123', 'farm')
	except:
		print('Fail to connect database.')
		conn.close()


def fireSuppression(ev=None):
	global fire_check

	print("Detected Flame!")
	fire_check = ON

	GPIO.output(PUMP, GPIO.HIGH)
	time.sleep(60)
	GPIO.output(PUMP, GPIO.LOW)

def fireSensor():
	global fire_check

	if(not GPIO.input(FLAME)):
		fireSuppression()
	else:
		fire_check = OFF

def moistureSensor():
	global pump_check, moisture_check, mois, moisture
	
	# Get data from arduino
	fromArduino = serial.Serial(port, 9600)
	fromArduino.flushInput()

	input_s = fromArduino.readline()
	moisture = 1024 - int(input_s)

	if(moisture != 9999 or moisture != None):
		if(moisture <= mois):
			moisture_check = ON
		else:
			moisture_check = OFF
	else:
		print('Cannot get moisture data from Arduino.')

	time.sleep(2)

def dhtSensor(model, sensor_pin):
	global temperature, humidity

	sensor, pin = (None, None)
	sensor_args = { 11: Adafruit_DHT.DHT11,
			22: Adafruit_DHT.DHT22,
			2302: Adafruit_DHT.AM2302 }
	if model in sensor_args:
		sensor = sensor_args[model]
		pin = sensor_pin

	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	if humidity is not None and temperature is not None:
		print('Temp={0:0.1f}* Humidity={1:0.1f}%'.format(temperature, humidity))
	else:
		print('Failed to get reading.')
		humidity, temperature = (9999, 9999)
	time.sleep(1)


# Working after sensing
def afterSensingTemp():
	global led_check, temp, temperature, temp_error

	# LED
	if(((temperature - temp) > temp_error) and led_check == ON):
		led_check = OFF
		print("LED OFF")
		GPIO.output(LED, GPIO.LOW)
		time.sleep(1)
	elif(((temperature - temp) < (-temp_error)) and led_check == OFF):
		led_check = ON
		print("LED ON")
		GPIO.output(LED, GPIO.HIGH)
		time.sleep(1)

def afterSensingHumi():
	global pump_check, humi, humidity, humi_error

	# PUMP
	if((((humidity - humi) > humi_error) and pump_check == ON) or fire_check == OFF or moisture_check == OFF):
		pump_check = OFF
		print("PUMP OFF")
		GPIO.output(PUMP, GPIO.LOW)
		time.sleep(2)
	elif(fire_check == ON or moisture_check == ON or (((humidity - humi) < (-humi_error)) and pump_check == OFF)):
		pump_check = ON
		print("PUMP ON")
		GPIO.output(PUMP, GPIO.HIGH)
		time.sleep(2)

def loop():
	global led_check, pump_check

	while True:
		fs = threading.Thread(target=fireSensor(), args=())
		fs.daemon = True
		fs.start()

		try:
			dhtSensor(11, 23)
		except:
			print("문제발생!")

		ah =  threading.Thread(target=afterSensingHumi(), args=())
		ah.daemon = True
		ah.start()

		at = threading.Thread(target=afterSensingTemp(), args=())
		at.daemon = True
		at.start()

		mt = threading.Thread(target=moistureSensor(), args=())
		mt.daemon = True
		mt.start()


@app.route('/')
def index():
	print(temperature, humidity)
	return render_template('index.html',
				temperature = temperature,
				humidity = humidity,
				temp = temp,
				humi = humi,
				led_check = led_check,
				pump_check = pump_check,
				moisture_check = moisture_check)

@app.route('/setting')
def setting():
	return render_template('setting.html',
				temp = temp,
				temp_error = temp_error,
				humi = humi,
				humi_error = humi_error,
				mois = mois,
				led_check = led_check,
				pump_check = pump_check,
				moisture_check = moisture_check)

@app.route('/PUT/DHT_Info', methods=['POST', 'GET'])
def DHT_Info(model, pin):
	global DHT_MODEL, DHT

	DHT_MODEL = model
	DHT = pin

	return None

@app.route('/GET/dht_Data', methods=['POST', 'GET'])
def getDHT():
	global temperature, humidity

#	dhtSensor(11, 23)
	return jsonify(temperature = temperature, humidity = humidity)

@app.route('/GET/STATUS', methods=['POST', 'GET'])
def getStatus():
	global led_light, temp, humi, mois, led_check, pump_check, moisture_check

	return jsonify(temp = temp, humi = humi, mois = mois, led_check = led_check, pump_check = pump_check, moisture_check = moisture_check)

@app.route('/PUT/SETTING', methods=['POST', 'GET'])
def putSetting():
	global conn

	title = str(request.json['title'])
	temp = int(request.json['temp'])
	temp_error = int(request.json['temp_error'])
	humi = int(request.json['humi'])
	humi_error = int(request.json['humi_error'])
	mois = int(request.json['mois'])
	
#	conn = MySQLdb.connect(host="192.168.0.225", user="pacaAl", passwd="pacaLover123", db="farm", port=3306)

	print("INPUT >>>", title, temp, temp_error, humi, humi_error, mois)
	if conn.cursor()is None:
		print('live')
	try:
		with conn.cursor() as cur:
			print('1111111111111')
			sql = "INSERT INTO setting (title, temp, temp_error, humi, humi_error, mois) VALUES ('%s', %d, %d, %d, %d, %d)" % (title, temp, temp_error, humi, humi_error, mois)
			#sql = "INSERT INTO setting (title, temp, temp_error, humi, humi_error, mois) VALUES (%s, %d, %d, %d, %d, %d)"
			print(sql)
			#print(conn.cursor().execute('select * from setting'))
			cur.execute(sql)
			conn.commit()
			print('return success')
			return 'SUCCESS'
	except:
		return 'ERROR'

@app.route('/GET/TITLES', methods=['POST', 'GET'])
def getTitles():
	global conn

	result = []
	try:
		with conn.cursor() as cur:
			sql = "SELECT title FROM setting"
			cur.execute(sql)
			rs = cur.fetchall()
			
			if(len(rs) is not 0):
				for item in rs:
					result.append(list(item))
				return jsonify(result)
	except:
		return 'ERROR'

@app.route('/GET/SETTING/<string:title>', methods=['POST', 'GET'])
def getSetting(title):
	global conn 

	result = []
	print("INPUT >>>", title)
	try:
		with conn.cursor() as cur:
			sql = "SELECT * FROM setting WHERE title = '%s'" % title
			cur.execute(sql)
			rs = cur.fetchone()

			for item in rs:
				result.append(list(item))

			return jsonify(rs)
	except:
		return 'ERROR'

@app.route('/PUT/SETTING_VALUE', methods=['POST', 'GET'])
def putSetting_Value():
	global temp, temp_error, humi, humi_error, mois

	temp = int(request.json['temp'])
	temp_error = int(request.json['temp_error'])
	humi = int(request.json['humi'])
	humi_error = int(request.json['humi_error'])
	mois = int(request.json['mois'])

	return 'SUCCESS'


if(__name__ == '__main__'):
	init()
	try:
		ts = threading.Thread(target=loop, args=())
		ts.daemon = True
		ts.start()
		
		app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
		GPIO.cleanup()
	except KeyboardInterrupt:
		GPIO.cleanup()
		print("END")
