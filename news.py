import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

def main():	
	news_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={코로나}'
	
	req = requests.get(news_url)
	soup = BeautifulSoup(req.text, 'html.parser')	
	
	news_dict = {}
	
	print()
	print('크롤링 중...')
	
	table = soup.find('ul',{'class' : 'list_news'})
	li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
	area_list = [li.find('div', {'class' : 'news_area'}) for li in li_list]
	a_list = [area.find('a', {'class' : 'news_tit'}) for area in area_list]
	title = a_list[0]['title']
	print(title)
	
	print('크롤링 완료')
	
	return title

