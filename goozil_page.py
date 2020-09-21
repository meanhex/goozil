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
    _pageHref = [x.get('href') for x in _href_results]
    _pageHref = list({x : x for x in _pageHref}.values()) # href 기준으로 중복을 제거
    _pageHref = sorted(_pageHref, key=lambda x : x[-1]) # href의 마지막 글자를 기준으로 정렬
    result = list()
    for _href in _pageHref :
        result.append({'no' : _href[_href.find('&page=') + 6], 'href' : _href})
    return result

if __name__ == '__manin__' :
    pages = find_page('http://swingingseoul.com/product/list.html?cate_no=45')

    for x in pages : 
        print(x['no'] + '_' + x['href'])
