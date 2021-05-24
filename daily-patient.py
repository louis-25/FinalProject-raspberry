import requests, json
import geolocation as location

url = requests.get("http://192.168.1.3:9091/speaker/daily-patient")
text = url.text
print(text)

data = json.loads(text)

print(data['live_date'])
print(data['sum'])

#live_date = data[0]
#print(live_date)

