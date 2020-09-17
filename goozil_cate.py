# ver proto2
# : 기존 text를 기준으로 찾아 href를 파싱하는것이 아닌, href의 조건을 기준으로 찾아 text, alt를 파싱하도록 수정
# : 기존 문제 1. text를 기준으로 검색해도 안나오면 조건을 추가적으로 달아야 했음
# : 기존 문제 2. 사이트 마다 category를 너무 다르게 사용함 (ex : [반팔,긴팔,니트], [아우터,가죽], [top], [outer] ... )
# : 개선 사항

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# ▼target class
class Link :
    def __init__(self, title, href) :
        super().__init__()
        self.title = title
        self.href = href
    def __setitem__(self, title, href) :
        self.title = title
        self.href = href

class Shop :
    def __init__(self, shop) :
        super().__init__()
        self.shop = shop
        self.title = ''
        self.links = list()
    def setLinks(self, links) :
        self.links = links
    def getLinks(self) :
        return self.links
    def show(self) :
        print('#%s' % self.title)
        for _link in self.links : 
            print('\t%-20s : %s' % (_link.title, _link.href))

# ▼ shop_list, tag_keys, cate_keys를 인자로 shop의 카테로리로 추정되는 link목록을 추가한 shop_list를 반환
def get_shoplist(_shop_list, _tag_keys, _cate_keys) :
    for _shop in _shop_list :
        bs = BeautifulSoup(_shop.shop, "html.parser")
        _shop.title = bs.head.title
        _body = bs.find('body')
        _cates = list()
        _href_results = list() # result for tag with href

        _href_results = _body.find_all(_tag_keys, href=_cate_keys)
        for result in _href_results :
            if len(result.text) > 2 :
                _cates.append(Link(result.text, result.get('href')))
            elif result.next != None and type(result) == type(result.next) : #!= None and result.next != '\n' :
                if len(result.next.text) > 2 :
                    _cates.append(Link(result.next.text, result.get('href')))
                elif 'alt' in result.next.attrs and len(result.next.attrs['alt']) > 0 :
                    _cates.append(Link(result.next.attrs['alt'], result.get('href')))
        if len(_cates) > 2 :
            _temp_cates = list({x.href : x for x in _cates}.values()) # href 기준으로 중복을 제거
            _temp_cates = sorted(_temp_cates, key=lambda x : len(x.href)) # href의 길이 순으로 정렬
            # for x in _temp_cates : 
            #     print('%s : %s' % (x.title, x.href))
            _shop.setLinks(_temp_cates)
        else : 
            print('cate length is short than 3')
    return _shop_list

shop_list = list() # stop list
shop_list.append(Shop(urlopen("http://www.da-sara.com/")))
shop_list.append(Shop(urlopen("http://www.swingingseoul.com/")))
shop_list.append(Shop(urlopen("http://www.smoothie-star.com/")))
shop_list.append(Shop(urlopen("http://www.melodystyle.co.kr/")))

tag_keys = list() # tag keyword list : tag for category
tag_keys.append('a')
tag_keys.append('img')

cate_words = list() # category keyword list : category for used item
cate_words.append(r'./list[.]+\w+[?].') # ~/list.□?~
cate_keys = [re.compile(x) for x in cate_words] # 정규식 추가

shop_list = get_shoplist(shop_list, tag_keys, cate_keys)
for x in shop_list : 
    x.show()