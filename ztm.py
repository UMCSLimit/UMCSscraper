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
    # Serialize hash, age, and cookie info for faster debugging
"""

class ZTM:
    def __init__(self):
        self.hash = ''
        self.age = ''
        self.cookie = ''
        self.last_updated = ''
        self.jsonData = json.dumps(default_json_response, default=date_handler)
        self.updateHeaders()

    def get_metadata(self):
        if len(hash) == 0:
            return json.dumps({ 'success': False })
        obj = {
            'success' : True,
            'last_updated': self.last_updated,
            'hash': self.hash,
            'age': self.age,
            'cookie': self.cookie
        }
        return json.dumps(obj, default=date_handler)

    def requestDeparture(self, id='757'):
        xml = get_xml_departure(hash=self.hash, id=id)
        xml_resp = requestSOAP(xml=xml, age=self.age, cookie=self.cookie, SOAPAction=ACTION)
        xml_parsed = xmltodict.parse(xml_resp)

        body = xml_parsed['soap:Envelope']['soap:Body']['CNR_GetRealDeparturesResponse']['CNR_GetRealDeparturesResult']['Schedules']
        
        stop = body['Stop']
        day = stop['Day']
        R = day['R']

        res_time = body['@time']
        res_name = stop['@name']
        res_id = stop['@id']
        res_type = day['@type']
        res_desc = day['@desc']

        vec_list = []

        for vec in R:
            vec_list.append(
                vec
            )

        new_json = {
            'success': True,
            'info': {
                'time': res_time,
                'name': res_name,
                'id': res_id,
                'desc': res_desc,
                'type': res_type
            },
            'payload': vec_list
        }
        
        # print(xml_parsed)
        # return json.dumps({
        #     'xml_parsed': xml_parsed,
        #     'body': body
        # })
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
    ztm.updateHeaders()
    xml_json = ztm.requestDeparture()
    print(xml_json)

# soup = BeautifulSoup(xml_resp)
# my_objects = soup.main.findAll("R", attrs={'attr':'DIR'})
# for my_object in my_objects:
#     print(my_object.contents)

# xml_street = """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetStreets xmlns='http://PublicService/'><s>""" + s + """</s></GetStreets></soap:Body></soap:Envelope>"""
# xml_stops =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetGoogleStops xmlns='http://PublicService/'><s>""" + s + """</s></GetGoogleStops></soap:Body></soap:Envelope>"""

# xml_route =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_RouteVariants xmlns='http://PublicService/'><n>3</n><vt></vt><s>""" + s + """</s></CNR_RouteVariants></soap:Body></soap:Envelope>"""
# xml_graph =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><DajGrafyGoogleKlient xmlns='http://PublicService/'><numer_lini>3</numer_lini><war_trasy>H</war_trasy><s>""" + s + """</s></DajGrafyGoogleKlient></soap:Body></soap:Envelope>"""
# xml_vech =   """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetVehicles xmlns='http://PublicService/'><r></r><d></d><nb>22291,9006,1812</nb><s>""" + s + """</s></CNR_GetVehicles></soap:Body></soap:Envelope>"""
# xml_dep =    """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetRealDepartures xmlns='http://PublicService/'><id>757</id><s>""" + s + """</s></CNR_GetRealDepartures></soap:Body></soap:Envelope>"""
