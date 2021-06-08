import requests, json
import geolocation as location

def main():
	result = location.main()
	params = {'r1': result[0], 'r2':result[1], 'r3':result[2]}
	url = "http://192.168.1.3:9091/speaker/getVaccineCenter"
	#res = requests.get("http://192.168.1.3:9091/speaker/getVaccineCenter", params)
	res = requests.post(url, params)
	return res.text



