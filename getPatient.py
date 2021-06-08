import requests, json

def patient(day, location): #일일 확진자수 데이터 받아오기
	url = ""
	if location == False:
		location = 'all'
	#url = requests.get("http://192.168.1.3:9091/speaker/getPatient?day=%s&location=%s" %(day, location))
	url = "http://192.168.1.3:9091/speaker/getPatient"
	myobj = {'day':day, 'location':location}
	result = requests.post(url, data = myobj)

	sum = 0
	text = result.text
	print("받아온 데이터 : ",text)

	if text == '결과값이 없습니다':
		sum = -1	
	else:
		data = json.loads(text)
		sum = data['sum']
		type(sum)
		print("확진자 수 : ", sum)

	return sum

def result(word_list):

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
				text = '오늘 확진자 수 가 아직 업데이트되지 않았습니다'
			else:
				text = '현재 확진자 수 %s명입니다' %(sum)
		elif '어제' in word_list:
			sum = patient('yesterday', check_loc)
			text = '어제 확진자수 %s명입니다' %(sum)
		else:
			sum = patient('today', 'all') #현재 전체 확진자 수
			if sum == -1:
				text = '오늘 확진자 수 가 아직 업데이트되지 않았습니다'
			else:
				text = '현재 확진자 수 %s명입니다' %(sum)

	else: #지역 물어봤을때
		if '오늘' in word_list: #covid_live에서 조회한다
			sum = patient('today', location[location2.index(check_loc)])
			text = '현재 %s지역 확진자수 %s명입니다' %(check_loc, sum)
		elif '어제' in word_list: #covid_result에서 조회한다
			print(check_loc)
			sum = patient('yesterday', check_loc)
			text = '어제 %s지역 확진자 수 %s명입니다' %(check_loc, sum)
		else:
			sum = patient('today', location[location2.index(check_loc)])
			text = '현재 %s지역 확진자 수 %s명입니다' %(check_loc, sum)

		if sum == -1:
			text = '%s지역 확진자 수 가 아직 업데이트 되지 않았습니다' %(check_loc)

	return text