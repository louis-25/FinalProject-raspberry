
import geolocation as location
import requests, json

def main():
	result = location.main()
	r1 = result[0]
	r2 = result[1]
	r3 = result[2]
	lat = result[3]
	lon = result[4]
	
	#url = requests.get("http://192.168.1.3:9091/speaker/weather?lat=%s&lon=%s" %(lat, lon))
	url = "http://192.168.1.3:9091/speaker/weather"
	param = {'lat': lat, 'lon': lon}
	result = requests.post(url, param)
	#url = requests.get("http://192.168.1.3:9091/speaker/weather?lat=37.4873799&lon=126.890367")
	text = '현재 ' + r1 +" "+ r2 +" "+ r3 + '은' +" "+ result.text
	print(text)
	
	return text