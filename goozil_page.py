# ver proto1
# : 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

import goozil_cate

def find_page(url) :
    bs = BeautifulSoup(urlopen(url), "html.parser")
    _body = bs.find('body')
    _href_results = _body.find_all('a', href=re.compile('.[&]page[=].'))
    result = [x.get('href') for x in _href_results]
    result = list({x : x for x in result}.values()) # href 기준으로 중복을 제거
    result = sorted(result, key=lambda x : x[-1]) # href의 마지막 글자를 기준으로 정렬
    return result

pages = find_page('http://swingingseoul.com/product/list.html?cate_no=45')

for x in pages : 
    print(x)
