#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from sel import getXMLheader

COOKIE_PREFIX = 'ASP.NET_SessionId='
ACTION = 'http://PublicService/CNR_GetRealDepartures'

# xml_street = """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetStreets xmlns='http://PublicService/'><s>""" + s + """</s></GetStreets></soap:Body></soap:Envelope>"""
# xml_stops =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetGoogleStops xmlns='http://PublicService/'><s>""" + s + """</s></GetGoogleStops></soap:Body></soap:Envelope>"""

# xml_route =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_RouteVariants xmlns='http://PublicService/'><n>3</n><vt></vt><s>""" + s + """</s></CNR_RouteVariants></soap:Body></soap:Envelope>"""
# xml_graph =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><DajGrafyGoogleKlient xmlns='http://PublicService/'><numer_lini>3</numer_lini><war_trasy>H</war_trasy><s>""" + s + """</s></DajGrafyGoogleKlient></soap:Body></soap:Envelope>"""
# xml_vech =   """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetVehicles xmlns='http://PublicService/'><r></r><d></d><nb>22291,9006,1812</nb><s>""" + s + """</s></CNR_GetVehicles></soap:Body></soap:Envelope>"""
# xml_dep =    """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetRealDepartures xmlns='http://PublicService/'><id>757</id><s>""" + s + """</s></CNR_GetRealDepartures></soap:Body></soap:Envelope>"""

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

class ZTM:
    def __init__(self):
        self.hash = ''
        self.age = ''
        self.cookie = ''
        self.updateHeaders()

    def requestDeparture(self, id='757'):
        xml = get_xml_departure(hash=self.hash, id=id)
        xml_resp = requestSOAP(xml=xml, age=self.age, cookie=self.cookie, SOAPAction=ACTION)
        return xml_resp
    
    def updateHeaders(self):
        headers = getXMLheader()
        self.hash = headers[0]
        self.age = '{}'.format(headers[1])
        self.cookie = COOKIE_PREFIX + headers[2]

if __name__ == "__main__":
    ztm = ZTM()
    ztm.updateHeaders()
    print(ztm.requestDeparture())

    # soup = BeautifulSoup(xml_resp)
    # my_objects = soup.main.findAll("R", attrs={'attr':'DIR'})
    # for my_object in my_objects:
    #     print(my_object.contents)
