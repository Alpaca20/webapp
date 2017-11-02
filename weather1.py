#coding:utf-8
from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

params= { "version":"1", "city":"부산", "county":"수영구", "village":"광안동" }
headers= { "appKey":"01684286-92bf-3309-8322-2728a14507f2" }

r = requests.get("http://apis.skplanetx.com/weather/current/hourly", params=params, headers=headers)

#print (r.json())
data = json.loads(r.text)
weather = data["weather"]["hourly"]
cTime = weather[0]["timeRelease"]
cSky = weather[0]["sky"]["name"]
cWind = weather[0]["wind"]["wspd"]
cTemp = weather[0]["temperature"]["tc"]

cWeather = "오늘의  날씨 " + cTime + " 기준하늘은 \'" + cSky + "\'이고 풍속은 " + cWind + ", 기온은 " + cTime + "입니다."
print (cWeather)

@app.route('/getWeather')
def getWeather():
	dic = json.loads(weather)
	return str(dic)

@app.route('/nowWeather')
def nowWeather():
	return cWeather

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=8888)
