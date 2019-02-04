#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import requests
import wget

xml = """<?xml version='1.0' encoding='utf-8'?><soap:Envelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xmlns:xsd='http://www.w3.org/2001/XMLSchema' xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'><soap:Body><CNR_GetRealDepartures xmlns='http://PublicService/'><id>299</id><s>jvr1uNhXYru0sMCOWXaqetAZmYk6ew7vcN1tl2AluEPU=</s></CNR_GetRealDepartures></soap:Body></soap:Envelope>"""
headers = {
    'Content-Type': 'text/xml;charset=UTF-8',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'Age': '12725',
    'Connection': 'keep-alive',
    'Content-Length': '387',
    'Cookie': 'ASP.NET_SessionId=jcafwmdaawlj0pp1soh0swum',
    'Host': 'www.sip.ztm.lublin.eu',
    'Origin': 'http://www.sip.ztm.lublin.eu',
    'Referer': 'http://www.sip.ztm.lublin.eu/',
    'SOAPAction': 'http://PublicService/CNR_GetRealDepartures',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',

    }

if __name__ == "__main__":
    print(requests.post('http://www.sip.ztm.lublin.eu/PublicService.asmx', data=xml, headers=headers).text)
