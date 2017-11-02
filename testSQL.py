import MySQLdb
from flask import Flask, render_template, request

app = Flask(__name__)

# DB connect setting
IP = '192.168.0.225'
UID = 'pacaAl'
PWD = 'pacaLover123'
DB = 'farm'
conn = None

def init():
	global conn

	try:
		conn = MySQLdb.connect(IP, UID, PWD, DB)
	except:
		if(conn != None):
			conn.close()
		print("Fail to connect DB.")

@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('testQuery.html');

@app.route('/GET/TITLE', methods=['POST', 'GET'])
def getTitle():
	global conn

	sql = "SELECT title FROM setting"
	result = []
	try:
		with conn.cursor() as cur:
			cur.execute(sql)
			rs = cur.fetchall()
			for item in rs:
				print("item", item)
				result.append(list(item))

				return result
	except:
		print("Fail to execute query.")
		return 'ERROR'

@app.route('/GET/SETTING/<string:title>', methods=['POST', 'GET'])
def getSetting(title):
	global conn

	sql = "SELECT * FROM setting WHERE 1=1 AND title = '%s'" % title
	result = []
	try:
		with conn.cursor() as cur:
			cur.execute(sql)
			rs = cur.fetchall()
			for item in rs:
				print("item2", item)
				result.append(list(item))
				return result
	except:
		print("Fail to execute query.")
		return 'ERROR'

if(__name__ == '__main__'):
	app.run(debug=True, host='0.0.0.0', port=8778, threaded=True)
