#!/usr/bin/env python
# -*- Encoding:UTF-8 -*- #
# coding=utf-8

import hashlib
import hmac
import base64
import requests
import time
import requests, json

# Signature Make
def make_signature(method, basestring, timestamp, access_key, secret_key):
    
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    signature = base64.b64encode(hmac.new(secret_key, message.encode('utf-8'), digestmod=hashlib.sha256).digest())
    
    return signature


def requestApi(timestamp, access_key, signature, uri):
	# Header for Request
	headers = {'x-ncp-apigw-timestamp': timestamp,
	'x-ncp-iam-access-key': access_key,
	'x-ncp-apigw-signature-v2': signature}
	
	# Geolocation API Request
	res = requests.get(uri, headers=headers)
	
	response = (res.content).decode('utf-8') #bytes -> str
	data = json.loads(response)
	geoLocation = data['geoLocation']
	result = [geoLocation["r1"],geoLocation["r2"],geoLocation["r3"]]
	#print(result)

	#print(geoLocation["lat"])
	#print(geoLocation["long"])
	#Check Response
	#print ('status : %d' % res.status_code)
	#print ('content : %s' % res.content)
	
	return result


def main():
	# Signature 생성에 필요한 항목
	url = requests.get("http://ip-api.com/json")
	data = json.loads(url.text)
	IP_ADDRESSS = data['query']
	method = "GET"
	basestring = "/geolocation/v2/geoLocation?ip=%s&ext=t&responseFormatType=json" %(IP_ADDRESSS)
	timestamp = str(int(time.time() * 1000))
	access_key = "CB1DD48857B03C6C8200"  # access key id (from portal or sub account)
	secret_key = bytes(str("133A2CAFBC1F4A6860EA5D253A264A0A0BAD66FB"),"utf8")  # secret key (from portal or sub account)
	signature = make_signature(method, basestring, timestamp, access_key, secret_key)
	
	# GET Request
	hostname = "https://geolocation.apigw.ntruss.com"	
	requestUri = hostname + basestring

	return requestApi(timestamp, access_key, signature, requestUri)
	

if __name__ == "__main__":
    main()
    
    

