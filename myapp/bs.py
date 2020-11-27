from bs4 import BeautifulSoup
from urllib.request import urlopen

response = urlopen('http://openapi.seoul.go.kr:8088/59506d537473696336306b6a795a70/xml/SPOP_LOCAL_RESD_DONG/1/5/20200617/%20/11110515')
soup = BeautifulSoup(response, 'html.parser')
for anchor in soup.find_all('row'):
    print(anchor.get('row'))

    
# url = ""

# request = urllib.request.urlopen(url)

# xml = request.read()

# soup = BeautifulSoup(xml, "html.parser")

# print(soup.find_all("row"))