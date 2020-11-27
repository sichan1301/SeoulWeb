import requests
import json
import xmltodict
import time

def weatherParse():
    city = "seoul"
    key = "4a2397410c5866ccc07efc4ea253ad55"
    url = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+key

    json_data = requests.get(url).content
    result = json.loads(json_data)

    return result


def coronaParse():
    url = "http://openapi.seoul.go.kr:8088/737063496a736963363564426b4b6b/xml/Corona19Status/1/5/"
    
    req = requests.get(url).content
    

    xmlObject = xmltodict.parse(req) 
    # xmldodict 라이브러리를 요청한 페이지의 url을 쪼개 객체를 형성

    allData = xmlObject['Corona19Status']['row']

    return allData

def popularParse():
    url ="http://openapi.seoul.go.kr:8088/59506d537473696336306b6a795a70/xml/SPOP_LOCAL_RESD_DONG/1/5/20200617/%20/11110515"

    req = requests.get(url).content

    xmlObject = xmltodict.parse(req)

    allData = xmlObject['SPOP_LOCAL_RESD_DONG']['row']

    return allData

def seoulParse():

    url = "http://swopenapi.seoul.go.kr/api/subway/454254455173696338334c546f5542/json/realtimeStationArrival/0/5/%EC%84%9C%EC%9A%B8"

    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result

def yongsanParse():

    url = "http://swopenapi.seoul.go.kr/api/subway/454254455173696338334c546f5542/json/realtimeStationArrival/0/5/%EC%9A%A9%EC%82%B0"
    
    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result


def centralParse():

    url = "http://swopenapi.seoul.go.kr/api/subway/454254455173696338334c546f5542/json/realtimeStationArrival/0/5/%EA%B3%A0%EC%86%8D%ED%84%B0%EB%AF%B8%EB%84%90"
    
    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result

def sooseoParse():

    url = "http://swopenapi.seoul.go.kr/api/subway/454254455173696338334c546f5542/json/realtimeStationArrival/0/5/%EA%B3%A0%EC%86%8D%ED%84%B0%EB%AF%B8%EB%84%90"
    
    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result

def dongseoulParse():

    url = "http://swopenapi.seoul.go.kr/api/subway/454254455173696338334c546f5542/json/realtimeStationArrival/0/5/%EA%B0%95%EB%B3%80"
    
    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result

def gangnamParse():

    url = "http://swopenapi.seoul.go.kr/api/subway/454254455173696338334c546f5542/json/realtimeStationArrival/0/5/%EA%B0%95%EB%82%A8"
    
    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result


def newsParse():

    url ="http://openapi.seoul.go.kr:8088/6d46586a617369633936446b465178/json/SeoulNewsList/1/5/"

    json_data = requests.get(url).content
    
    result = json.loads(json_data)
    
    return result