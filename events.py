from bs4 import BeautifulSoup
import requests
import json
import datetime
import time 
from helpers import date_handler, default_json_response
from flask import Response
from requests import get
from scrape import getColor

#TO DO:
# 1. object orient everything
# 2. scrape url of the event
# 3. scrape description from url scraped in #2
# 4. failcheck after len of all_events is diffrent than it supposed to be
"""


def check_if_good(self):
	if (self.event_name == "") or (self.date == "") or (self.type == "") or (self.color == ""):
		return False
	else:
		return True
def serialize_to_json(self):
	return json.dumps(self.itemList)
	

"""

def events():
	url= 'http://www.umcs.pl'
	response = get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	all_events = []
	all_events = soup.find_all('a', class_='box-event-small')
	i=0
	id = i
	failflag = False
	itemList = []
	for item in all_events:
		event_name = item.find('div', class_='col-xs-7')
		event_name = event_name.text.replace('\n', '').strip()
				
		date = item.find('em', class_='label-meta')
		date = date.text.replace('\n', '').strip()
		
		type = item.find('em', class_='label-area-A')
		type = type.text.replace('\n', '').strip()
		
		color = getColor(type)
		# check for fails in scraping
		if (event_name == "") or (date == "") or (type == "") or (color == ""):
			failflag = True

		# serialize data to JSON format
		if not failflag:	
			itemList.append({
				'name': event_name,
				'date': date,
				'type': type,
				'color': color
			})
	return Response(
		response=json.dumps(itemList),
		status=200,
		mimetype='application/json'
	)
if __name__ == '__main__':
	events()