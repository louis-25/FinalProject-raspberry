#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function

import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import MicrophoneStream as MS
import RPi.GPIO as GPIO
import ktkws # KWS
import user_auth as UA
import audioop
import os
import requests, json
import location
import ex5_queryText as dialog # 서버에서 답변가져오기
from requests import get
from ctypes import *

#서버 연결정보
HOST = 'gate.gigagenie.ai'
PORT = 4080

KWSID = ['기가지니', '지니야', '친구야', '자기야']
RATE = 16000
CHUNK = 512

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
btn_status = False

def callback(channel):  
	print("falling edge detected from pin {}".format(channel))
	global btn_status
	btn_status = True
	print(btn_status)

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

#에러처리부분
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def generate_request():
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
    
        for content in audio_generator:
            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            yield message
            
            rms = audioop.rms(content,2)
            #print_rms(rms)


def getVoice2Text():	
    print ("\n\n음성인식을 시작합니다.\n\n종료하시려면 Ctrl+\ 키를 누루세요.\n\n\n")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials()) #API Key사용
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request()
    resultText = ''
    for response in stub.getVoice2Text(request):
        if response.resultCd == 200: # partial
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
        elif response.resultCd == 201: # final
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
            break
        else:
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            break

    print ("\n\n인식결과: %s \n\n\n" % (resultText))
    return resultText

# TTS : getText2VoiceStream
def getText2VoiceStream(inText,inFileName):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	writeFile=open(inFileName,'wb')
	for response in stub.getText2VoiceStream(message):
		if response.HasField("resOptions"):
			print ("\n\nResVoiceResult: %d" %(response.resOptions.resultCd))
		if response.HasField("audioContent"):
			print ("Audio Stream\n\n")
			writeFile.write(response.audioContent)
	writeFile.close()
	return response.resOptions.resultCd

def detect():
	with MS.MicrophoneStream(RATE, CHUNK) as stream: #서버로 보낸다
		audio_generator = stream.generator()

		for content in audio_generator:

			rc = ktkws.detect(content)
			rms = audioop.rms(content,2) #오디오형태로 변환
			#print('audio rms = %d' % (rms))

			if (rc == 1):
				MS.play_file("./data/sample_yes.wav")
				return 200

def btn_detect():
	global btn_status
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()
		GPIO.output(31, GPIO.HIGH)
		for content in audio_generator:
#			GPIO.output(31, GPIO.HIGH)
			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			print('audio rms = %d' % (rms))
#			GPIO.output(31, GPIO.LOW)
			if (btn_status == True):
				rc = 1
				btn_status = False			
			if (rc == 1):
				GPIO.output(31, GPIO.HIGH)
				MS.play_file("./data/sample_yes.wav")
				GPIO.output(31, GPIO.LOW)
				return 200

def test(key_word = '기가지니'): #기본값 : 기가지니
	rc = ktkws.init("./data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n호출어를 불러보세요~\n')
	ktkws.set_keyword(KWSID.index(key_word))
	rc = detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	result_test()
	ktkws.stop()
	return rc

def btn_test(key_word = '기가지니'):
	global btn_status
	rc = ktkws.init("./data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n버튼을 눌러보세요~\n')
	ktkws.set_keyword(KWSID.index(key_word))
	rc = btn_detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc

# DIALOG : queryByText
def queryByText(text):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqQueryText()
	message.queryText = text
	message.userSession = "1234"
	message.deviceId = "yourdevice"
		

	response = stub.queryByText(message)

	print ("\n\nresultCd: %d" % (response.resultCd))
	if response.resultCd == 200:
		print ("\n\n\n질의한 내용: %s" % (response.uword))
		#dssAction = response.action
		for a in response.action:
			response = a.mesg
		parsing_resp = response.replace('<![CDATA[', '')
		parsing_resp = parsing_resp.replace(']]>', '')
		print("\n\n질의에 대한 답변: " + parsing_resp + '\n\n\n')
		#return response.url
		return parsing_resp
	else:
		print ("Fail: %d" % (response.resultCd))
		#return None

def patient(day, location): #일일 확진자수 데이터 받아오기
	url = ""

	url = requests.get("http://192.168.1.3:9091/speaker/patient?day=%s&location=%s" %(day, location))

	sum = 0
	text = url.text
	print("받아온 데이터 : ",text)

	if text == '결과값이 없습니다':
		sum = -1	
	else:
		data = json.loads(text)
		sum = data['sum']
		type(sum)
		print("확진자 수 : ", sum)

	return sum

#def location_

def speaker_ip():#스피커 기준 ip주소 받아오기
	ip = get("https://api.ipify.org").text
	print("My public IP address : ", ip)


def patient_result(word_list):

	#covid_live
	location = ["seoul", "incheon", "gwangju", "daejeon", "daegu", "busan", "ulsan", "sejong",
				"gyeonggi", "gangwon", "chungbuk", "chungnam", "jeonbuk", "jeonnam", "gyeongbuk", 
				"gyeongnam", "jeju"]

	#covid_result
	location2 = ["서울", "인천", "광주", "대전", "대구", "부산", "울산", "세종", "경기", 
					"강원", "충북", "충남","전북", "전남", "경북", "경남", "제주"]
	
	check_loc = False
	for loc in word_list: 
		if loc in location2: #사용자 발화에서 지역관련 단어가 있을때
			check_loc = loc

	if check_loc == False: #지역 안물어봤을때
		if '오늘' in word_list:
			sum = patient('today', 'all') #현재 전체 확진자수
			if sum == -1:
				text = '오늘 확진자수가 아직 업데이트되지 않았습니다'
			else:
				text = '현재 확진자수 %s명입니다' %(sum)
		elif '어제' in word_list:
			sum = patient('yesterday', check_loc)
			text = '어제 확진자수 %s명입니다' %(sum)
		else:
			sum = patient('today', 'all') #현재 전체 확진자수
			if sum == -1:
				text = '오늘 확진자수가 아직 업데이트되지 않았습니다'
			else:
				text = '현재 확진자수 %s명입니다' %(sum)

	else: #지역 물어봤을때
		if '오늘' in word_list: #covid_live에서 조회한다
			sum = patient('today', location[location2.index(check_loc)])
			text = '현재 %s지역 확진자수 %s명입니다' %(check_loc, sum)
		elif '어제' in word_list: #covid_result에서 조회한다
			print(check_loc)
			sum = patient('yesterday', check_loc)
			text = '어제 %s지역 확진자수 %s명입니다' %(check_loc, sum)
		else:
			sum = patient('today', location[location2.index(check_loc)])
			text = '현재 %s지역 확진자수 %s명입니다' %(check_loc, sum)


	return text

	
def main():
   # STT

#	text = '오늘 인천 지역 확진자 수 알려줘'
#	word_list = text.split(' ')
#	text = location_result(word_list)
#	print(text)

#	for one in word_list:
#		if one in location:
#			print(one)
#	print(location.contains())

	while True:
		btn_test()
		text = ''
		text = getVoice2Text()
		print(text)
		word_list = text.split(' ')
#		location = ['서울', '부산', '대구', '인천', '광주', '대전']
		print(word_list)
	
		if ('코로나'  in word_list) or ('확진자' in word_list):
			text = patient_result(word_list)
		elif '진료소' in word_list:
			result = location.main()
			text = '현재 가장 가까운 진료소는 %s 입니다' %(result) #가까운 진료소 알려줘
		else:
			text = dialog.queryByText(text)

		print("if문 : ",text)
		output_file = "voicetest.wav"
		getText2VoiceStream(text,output_file)
		MS.play_file(output_file)

if __name__ == '__main__':
    main()
