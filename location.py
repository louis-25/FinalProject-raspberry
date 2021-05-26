import requests, json
import geolocation as location

'''
result = location.main()
print(result)
requests.get("http://192.168.1.3:9091/speaker/triage?r1={r1}&r2={r2}&r3={r3}"
.format(r1=result[0], r2=result[1], r3=result[2]))
'''
def main():
	result = location.main()
	params = {'r1': result[0], 'r2':result[1], 'r3':result[2]}
	res = requests.get("http://192.168.1.3:9091/speaker/triage", params)
	return res.text



