import requests, json
import geolocation as location

def main():
	result = location.main()
	params = {'r1': result[0], 'r2':result[1], 'r3':result[2]}
	url = "https://corona-114.kro.kr/speaker/getVaccineCenter"
	#res = requests.get("http://192.168.1.3:9091/speaker/getVaccineCenter", params)
	res = requests.post(url, params)
	print('r1 : %s r2 : %s r3 : %s ' %(result[0], result[1], result[2]))
	data = json.loads(res.text)
	print('진료소 : ' , data['Facility'])
	print('주소 : ' , data['Address'])
	return data



