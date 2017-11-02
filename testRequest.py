import MySQLdb
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('ajax.html')

@app.route('/test', methods=['POST', 'GET'])
def test():
	name = request.args.get('name', 'aaaa', type=str)
#	name = request.json['name']
	return "it works! ~'%s'~" % name

if(__name__ == '__main__'):
	app.run(debug=True, host='0.0.0.0', port=8887, threaded=True)
