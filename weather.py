
import geolocation as location

result = location.main()
print(result)
'''
import requests
from bs4 import BeautifulSoup
import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
 
 
source = requests.get('https://www.weather.go.kr/weather/observation/currentweather.jsp')
soup = BeautifulSoup(source.content,"html.parser")
 
table = soup.find('table',{'class':'table_develop3'})
data = []
 
print("#"*30)
print("\nHello! Here's today's weather!\n")
print("#"*30)
 
for tr in table.find_all('tr'):
    tds = list(tr.find_all('td'))
    for td in tds:
        if td.find('a'):
            point = td.find('a').text
            temp = tds[5].text
            humidity = tds[9].text
            print("{0:<7} {1:<7} {2:<7}".format(point,temp,humidity))
            data.append([point,temp,humidity])
 
print("#"*30)
print("\nIt ends here. thanks!\n")
print("#"*30)
 
print(data)
'''