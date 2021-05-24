import requests, json

#url = requests.get("http://192.168.1.3:9091/speaker/daily-patient")
#Google geolocation api
url = requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAul55HBi9_DCpZVtCDwmi4PDmgt3Y-7Os")

#url = requests.get("http://ip-api.com/json") #공인ip주소

#url = requests.post("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode")
text = url.text
print(text)

data = json.loads(text)

#print(data['query']) #
#print(data['location'])
print(data['location']['lat'])
print(data['location']['lng'])


#print(data['live_date'])
#print(data['sum'])


#live_date = data[0]
#print(live_date)

