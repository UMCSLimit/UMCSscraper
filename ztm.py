#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from sel import getXMLheader
import xmltodict, json
from helpers import default_json_response, date_handler
import datetime

COOKIE_PREFIX = 'ASP.NET_SessionId='
ACTION = 'http://PublicService/CNR_GetRealDepartures'

def get_xml_departure(hash='', id=''):
    xml = """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetRealDepartures xmlns='http://PublicService/'><id>""" + '{}'.format(id) + """</id><s>""" + hash + """</s></CNR_GetRealDepartures></soap:Body></soap:Envelope>"""
    return xml

def requestSOAP(xml='', age='', cookie='', SOAPAction=''):
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Age': age,
        'Connection': 'keep-alive',
        'Content-Length': '{}'.format(len(xml)),
        'Cookie': cookie,
        'Host': 'www.sip.ztm.lublin.eu',
        'Origin': 'http://www.sip.ztm.lublin.eu',
        'Referer': 'http://www.sip.ztm.lublin.eu/',
        'SOAPAction': SOAPAction,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

    xml_resp = requests.post(
        'http://www.sip.ztm.lublin.eu/PublicService.asmx',
        data=xml,
        headers=headers
        ).text

    return xml_resp

"""
    To do:
    # Refactor requestDeparture
    # Clean up data from xml
    # Check for bugs when serializing
    # Fix check_if_request_works
"""

class ZTM:
    def __init__(self):
        self.hash = ''
        self.age = ''
        self.cookie = ''
        self.last_updated = ''
        self.jsonData = json.dumps(default_json_response, default=date_handler)
        # working_headers = self.load_from_file()
        # if working_headers:
        #     print("Working!")
        self.updateHeaders()
        # else:
        #     print("Headers not working..")
        #     self.save_to_file()

    def save_to_file(self):
        try:
            my_file = open('headers.txt', 'w')
            my_file.write(self.hash + '\n')
            my_file.write(str(self.age) + '\n')
            my_file.write(self.cookie + '\n') 
        except:
            print("Error saving headers")

    def load_from_file(self):
        try:
            my_file = open("headers.txt", "r")
            headers = my_file.read().split("\n")
            self.hash = headers[0]
            self.age = headers[1]
            self.cookie = headers[2]
            working_request = self.check_if_request_works()
            return working_request
        except:
            return False

    def check_if_request_works(self):
        # TO DO ! IMPORTANT
        # tmp = self.requestDeparture()
        return True

    def get_metadata(self):
        if len(self.hash) == 0:
            return json.dumps({ 'success': False, 'payload': []})
        obj = {
            'success' : True,
            'last_updated': self.last_updated,
            'hash': self.hash,
            'age': self.age,
            'cookie': self.cookie
        }
        return json.dumps(obj, default=date_handler)

    def buses(self, req={}):
        buses = req['buses']
        buses_to_add = []
        for id in buses:
            buses_to_add.append(self.getBusStop(id))
        new_json = {
            'success': True,
            'info': {
            },
            'payload': buses_to_add
        }
        return json.dumps(new_json)

    def getBusStop(self, id='757'):
        xml = get_xml_departure(hash=self.hash, id=id)
        xml_resp = requestSOAP(xml=xml, age=self.age, cookie=self.cookie, SOAPAction=ACTION)
        xml_parsed = xmltodict.parse(xml_resp)
        body = xml_parsed['soap:Envelope']['soap:Body']['CNR_GetRealDeparturesResponse']['CNR_GetRealDeparturesResult']['Schedules']
        stop = body['Stop']
        day = stop['Day']
        R = day['R']
        # type ? 
        vec_list = []
        for vec in R:
            is_bus = True if vec['@vt'].find('A') != -1 else False
            has_air_conditioning = True if vec['@vuw'].find('K') != -1 else False
            has_ticket_machine = True if vec['@vuw'].find('B') != -1 else False
            is_low_floor = True if vec['@vuw'].find('N') != -1 else False
            is_planned = True if vec['S']['@t'].strip().find(' ') != -1 else False
            # vec -> N and T ? 
            vec_list.append({
                    'number': vec['@nr'],
                    'direction': vec['@dir'],
                    'time': vec['S']['@t'],
                    'time_adv': vec['S']['@tm'],
                    'planned': is_planned,
                    'properties': {
                        'bus': is_bus,
                        'ticket_machine': has_ticket_machine,
                        'air_conditioning': has_air_conditioning,
                        'low_floor': is_low_floor
                    },
                    'advanced': {
                        'vt': vec['@vt'],
                        'vuw': vec['@vuw'],
                        'th': vec['S']['@th'],
                        'm': vec['S']['@m'],
                        's': vec['S']['@s'],
                        'id': vec['S']['@id'],
                        'nb': vec['S']['@nb'],
                        'veh': vec['S']['@veh'],
                        'uw': vec['S']['@uw'],
                        'kuw': vec['S']['@kuw'],
                    }
            })
        return {
            'info': {
            'time': body['@time'],
            'name': stop['@name'],
            'id': stop['@id'],
            'desc': day['@desc'],
            'type': day['@type']
            },
            'payload': vec_list
        }

    def requestDeparture(self, id='757'):
        bus = self.getBusStop(id)
        new_json = {
            'success': True,
            'info': bus['info'],
            'payload': bus['payload']
        }
        return json.dumps(new_json, default=date_handler)
    
    def updateHeaders(self):
        try:
            headers = getXMLheader()
            self.last_updated = datetime.datetime.now()
            self.hash = headers[0]
            self.age = '{}'.format(headers[1])
            self.cookie = COOKIE_PREFIX + headers[2]
        except:
            print('Error opening website')

if __name__ == "__main__":
    ztm = ZTM()