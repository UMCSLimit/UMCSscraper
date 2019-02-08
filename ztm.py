#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from sel import getXMLheader

s = """RHz1iE+zHloyAg57QR8yxjpBmxzdKaGnE9qWeMbSNM9w="""
AGE = '469'

COOKIE_PREFIX = 'ASP.NET_SessionId='
COOKIE = ''
ACTION = 'http://PublicService/CNR_GetRealDepartures'

# no age
xml_street = """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetStreets xmlns='http://PublicService/'><s>""" + s + """</s></GetStreets></soap:Body></soap:Envelope>"""
xml_stops =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><GetGoogleStops xmlns='http://PublicService/'><s>""" + s + """</s></GetGoogleStops></soap:Body></soap:Envelope>"""
# one route with out age
# age
xml_route =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_RouteVariants xmlns='http://PublicService/'><n>3</n><vt></vt><s>""" + s + """</s></CNR_RouteVariants></soap:Body></soap:Envelope>"""
xml_graph =  """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><DajGrafyGoogleKlient xmlns='http://PublicService/'><numer_lini>3</numer_lini><war_trasy>H</war_trasy><s>""" + s + """</s></DajGrafyGoogleKlient></soap:Body></soap:Envelope>"""
xml_vech =   """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetVehicles xmlns='http://PublicService/'><r></r><d></d><nb>22291,9006,1812</nb><s>""" + s + """</s></CNR_GetVehicles></soap:Body></soap:Envelope>"""
xml_dep =    """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetRealDepartures xmlns='http://PublicService/'><id>757</id><s>""" + s + """</s></CNR_GetRealDepartures></soap:Body></soap:Envelope>"""

def requestSOAP(xml = '', SOAPAction=''):
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'Age': AGE,
        'Connection': 'keep-alive',
        'Content-Length': '{}'.format(len(xml)),
        'Cookie': COOKIE,
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

if __name__ == "__main__":
    headers = getXMLheader()
    s = headers[0]
    AGE = '{}'.format(headers[1])
    COOKIE = COOKIE_PREFIX + headers[2]
    resp = requestSOAP(xml=xml_dep, SOAPAction=ACTION)
    print(resp)
    # print(requestSOAP(xml=xml_street, SOAPAction='http://PublicService/GetStreets'))
    # time.sleep(5)
    # print(requestSOAP(xml=xml_stops, SOAPAction='http://PublicService/GetGoogleStops'))
    # time.sleep(5)
    # print(requestSOAP(xml=xml_route, SOAPAction='http://PublicService/GetRoutes'))
    # time.sleep(5)
    # print(requestSOAP(xml=xml_route, SOAPAction='http://PublicService/CNR_RouteVariants'))
    # time.sleep(5)
    # print(requestSOAP(xml=xml_graph, SOAPAction='http://PublicService/DajGrafyGoogleKlient'))
    # time.sleep(5)
    # print(requestSOAP(xml=xml_dep, SOAPAction='http://PublicService/CNR_GetRealDepartures'))
    # time.sleep(5)
    # print(requestSOAP(xml=xml_vech, SOAPAction='http://PublicService/CNR_GetVehicles'))

    # soup = BeautifulSoup(xml_resp)
    # my_objects = soup.main.findAll("R", attrs={'attr':'DIR'})
    # for my_object in my_objects:
    #     print(my_object.contents)
