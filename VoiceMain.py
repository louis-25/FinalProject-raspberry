#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function

import MicrophoneStream as MS
import getVaccineCenter # 현재 위치에서 가장 가까운 진료소
import getPatient # 코로나 확진자 수
import ex5_queryText as dialog # KT서버에 저장된 답변
import getWeather #현재 접속지역 날씨정보 받아오기
import getNews #코로나 최신뉴스 받아오기
import VoiceService as service # 음성인식 서비스
	
def main():

	news_keyword = ['코로나', '날씨', '연애', '건강', '취업', '주식', '경제', '코인']

	while True:
		service.btn_test()
		text = ''
		text = service.getVoice2Text()
		print(text)
		word_list = text.split(' ')
		print(word_list)

		if '뉴스' in word_list:
			print('word: ',word_list)
			for keyword in news_keyword:
				if keyword in word_list:	
					print('keyword: ',keyword)				
					text = getNews.main(keyword)
					break
			
		elif ('코로나'  in word_list) or ('확진자' in word_list) or ('확진' in word_list):
			text = getPatient.result(word_list)
		elif '진료소' in word_list:
			result = getVaccineCenter.main()
			text = '현재 가장 가까운 진료소는 %s 입니다' %(result) #가까운 진료소 알려줘
		elif '날씨' in word_list:
			text = getWeather.main()
		
		else:
			text = dialog.queryByText(text)

		print("if문 : ",text)
		output_file = "voicetest.wav"
		service.getText2VoiceStream(text,output_file)
		MS.play_file(output_file)

if __name__ == '__main__':
    main()
