from bs4 import BeautifulSoup
import requests
import json
import datetime
import time 
from helpers import date_handler, default_json_response
from flask import Response
from requests import get
from scrape import getColor


def main():
	url= 'http://www.umcs.pl'
	response = get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	all_events = []
	all_events = soup.find_all('a', class_='box-event-small')
	i=0
	id = i
	for item in all_events:
		event_name = item.find('div', class_='col-xs-7')
		event_name = event_name.text.replace('\n', '').strip()
				
		date = item.find('em', class_='label-meta')
		date = date.text.replace('\n', '').strip()
		
		type = item.find('em', class_='label-area-A')
		type = type.text.replace('\n', '').strip()
		
		color = getColor(type)

		# serialize data
		print(id)
		print(event_name)
		print(date)
		print(type)
		print(color)
		id = id+1
if __name__ == '__main__':
	main()