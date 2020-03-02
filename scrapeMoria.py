#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import time,datetime

from helpers import date_handler, default_json_response
from flask import Response
ActivityList = []
iter = 0
class Acitvity:
    def __init__(self, id, name, timeStart, timeEnd, breakTime, isOneTime, month, day):
        self.id = id
        self.name = name
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.breakTime = breakTime
        self.isOneTime = isOneTime
        self.day = day
        self.month = month

def getWeekDayFromPolish(weekdayInPolish):
    if weekdayInPolish == 'poniedziałek':
        return 0
    elif weekdayInPolish == 'wtorek':
        return 1
    elif weekdayInPolish == 'środa':
        return 2
    elif weekdayInPolish == 'czwartek':
        return 3
    elif weekdayInPolish == 'piątek':
        return 4
    # sobota / niedziela to be implemented
def getPolishWeekDayFromInt(id):
    if id == 0:
        return 'poniedziałek'
    elif id == 1:
        return 'wtorek'
    elif id == 2:
        return 'środa'
    elif id == 3:
        return 'czwartek'
    elif id == 4:
        return 'piątek'   

def MoriaScraper(id):
    iter = 0
    ActivityList.clear()
    currtime = datetime.datetime.today()
    curr_weekday = currtime.weekday()
    stringWeekDay = getPolishWeekDayFromInt(curr_weekday)
    url = 'http://moria.umcs.lublin.pl/room/' + str(id)
   # print(url)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    all_activities = soup.find_all(  'div', attrs={'class':'activity_block','data-weekdaytext' : stringWeekDay}   )
    print(len(all_activities))
    if len(all_activities) == 0:
        ActivityList.append(Acitvity(0,'Brak zajec', '00:00', '00:00', 0,0, 0,0))
        ActivityList.append(Acitvity(1,'Brak zajec', '00:00', '00:00', 0,0,0,0))
    else:
        print(all_activities)
        for activ in all_activities:
            # get title
            divs = activ.find_all('div', attrs={'class':'activity_block_top'})
            _title = divs[0].find_all('a', title=True, attrs={'class': 'subject'})
            title = _title[0]['title'] # TITLE
            # get time start
            timeStart = activ['data-starttime']
            timeEnd = activ['data-endtime']
            breakTime = activ['data-breaktime']
            # check if it is only one time
            oneTimeFlag = False
            onetime = activ.find('a', attrs={'title':'0i Zaj. jednorazowe M\DD'})
            #print(onetime)
            if onetime:
                oneTimeFlag = True
                # extract date and time from title
                try:
                    ActivityList.append(Acitvity
                    (iter,title,timeStart,timeEnd, breakTime,oneTimeFlag, int(title[0:1]), int(title[2:4])))
                    iter+=1
                except ValueError:
                    ActivityList.append(Acitvity
                    (iter,title,timeStart,timeEnd, breakTime,0, 0, 0))
                    iter+=1
            else:
                ActivityList.append(Acitvity(iter,title,timeStart,timeEnd, breakTime,oneTimeFlag, 0, 0))
                iter+=1
            # ActivityList.append({
            #     'id': iter,
            #     'title': title,
            #     'timeStart': timeStart,
            #     'timeEnd': timeEnd
            # })

   # aula = json.dumps(ActivityList)
   # return Response(
	#	response=aula,
	#	status=200,
	#	mimetype='application/json'
#	)
def getClosestTwo(activity_list):
    mindiff =0
    indeks =0
    i=0
    # aktualny time w sekundach < time w ac
    foundAny = False
    for ac in activity_list:
        ftr = [36000,3600,60]
        time = ac.timeStart
        sectime = int(ac.timeStart[0]) * 36000
        sectime += int(ac.timeStart[1]) * 3600
        sectime += int(ac.timeStart[3]) * 60
        sectime += int (ac.timeStart[4])
        now = datetime.datetime.now()
        currtime = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        #print('sectime: ' + str(sectime)) 
        #print(sectime > currtime)
        #print('currtime: ' + str(currtime))
        #print(ac.isOneTime)
        #print('acmonth: ' + str(ac.month) + 'nowmonth: ' + str(now.month))
        #print(ac.month == now.month)
        #print('acday: ' + str(ac.day) + 'nowday: ' + str(now.day))
        #print('\n')
        if sectime > currtime and not ac.isOneTime:
            foundAny = True
            break
        elif sectime > currtime and ac.isOneTime: 
            if now.month == ac.month and now.day == ac.day: 
                foundAny = True       
                break
        else:
            indeks+=1
    if not foundAny: # Przypadek w którym nie ma dostępnego POPRAWNEGO zajęcia w dniu
        indeks = 0
        for ac in activity_list:
            ftr = [3600,60,1]
            time = ac.timeStart
            sectime = sum([a*b for a,b in zip(ftr, map(int,time.split(':')))])
            now = datetime.datetime.now()
            currtime = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
            if sectime > currtime:
                foundAny = True
                break
            else:
                indeks+=1  
    if indeks == len(activity_list):
        indeks = 0
    #print(indeks)
    FinalList = []
    FinalList.append({
        'id': 0,
        'title': activity_list[indeks].name,
        'timeStart': activity_list[indeks].timeStart,
        'timeEnd': activity_list[indeks].timeEnd,
        'isOneTime': activity_list[indeks].isOneTime
    })
    listlength = len(activity_list)
    begindex = indeks%listlength
    print('Begin indeks: ' + str(begindex))
    while activity_list[(indeks)%listlength].isOneTime and (now.month != activity_list[(indeks)%listlength].month or now.day != activity_list[(indeks)%listlength].day):
        #print('while')
        indeks+=1
        #print(indeks)
        #print(begindex)
        if indeks%listlength == begindex:
            indeks = begindex
            break
    indeks+=1
    FinalList.append({
        'id': 1,
        'title': activity_list[(indeks)%listlength].name,
        'timeStart': activity_list[(indeks)%listlength].timeStart,
        'timeEnd': activity_list[(indeks)%listlength].timeEnd,
        'isOneTime': activity_list[(indeks)%listlength].isOneTime
    })
    aula = json.dumps(FinalList)
    return Response(
		response=aula,
		status=200,
		mimetype='application/json'
	)
def getActivities():
    scrap = MoriaScraper(30)
    ret = getClosestTwo(ActivityList)
    return ret
if __name__ == '__main__':
    scrap = MoriaScraper(30)
    getClosestTwo(ActivityList)

