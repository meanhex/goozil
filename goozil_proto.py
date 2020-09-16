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


# ▼배열의 모든 str을 lower, upper, capitalize한 배열로 수정
def crate_allword(x) :
    if len(x) <= 0 :
        return None
    exlist = list()
    exlist.extend(x.lower() for x in x)
    exlist.extend(x.upper() for x in x)
    exlist.extend(x.capitalize() for x in x)
    return exlist

shop_list = list() # stop list
shop_list.append(urlopen("http://www.da-sara.com/"))
shop_list.append(urlopen("http://www.swingingseoul.com/"))
shop_list.append(urlopen("http://www.smoothie-star.com/"))
shop_list.append(urlopen("http://www.melodystyle.co.kr/"))

bs_objs = [BeautifulSoup(x, "html.parser") for x in shop_list]

tag_words = list() # tag keyword list : tag for category
tag_words.append('a')
tag_words.append('img')
tag_words.append('li')

category_words = list() # category keyword list : category for used item
category_words.append('men')
category_words.append('women')
category_words.append('new')
category_words.append('outer')
category_words.append('top')
category_words.append('bottom')
category_words.append('acc')
category_words.append('bag')
category_words.append('shoes')
category_words.append('accesory')
category_words.append('premium')
category_words.append('boutique')
category_words = crate_allword(category_words)
category_keys = [re.compile(x + '$') for x in category_words] # 정규식 추가

category_none_words = list()
category_none_words.append('category')
category_none_words.append('cate')
category_none_words = crate_allword(category_none_words)
category_none_keys = [re.compile(x + '$') for x in category_none_words] # 정규식 추가


for bs in bs_objs :
    print(bs.head.title)
    _body = bs.find('body')
    _categorys = list()
    _try_text_results = list() # result for categorys with href in tags
    _try_alt_results = list()
    _try_none_results = list()

    # ▼ tag = a search : category 정보가 a tag의 text가 가지고 있을때
    _try_text_results = _body.find_all(tag_words, text=category_keys, href=re.compile('.'))
    if len(_try_text_results) > 0 :
        # 태그 정보는 dict들로 구성되어 있음
        #_categorys.extend(Link(x.text, x.get('href')) for x in _try_text_results)
        _categorys.append([Link(x.text, x.get('href')) for x in _try_text_results])
        print('%d' % 1)
        
    # ▼ tag = a in alt search : category 정보를 a tag 자식의 alt가 가지고 있을때
    _try_alt_results = _body.find_all(tag_words, alt=category_keys)
    if len(_try_alt_results) > 0 :
        _categorys.append([Link(x.attrs['alt'], x.find_parent('a').get('href')) for x in _try_alt_results])
        print('%d' % 2)

    # ▼ tag = li in each category search : 대분류 링크 없이 소분류로 표시되는 경우
    _try_none_results = _body.find_all(tag_words, text=category_none_keys)
    if len(_try_none_results) > 0 :
        for _results in _try_none_results :
            _parent = _results.parent('a')
            _categorys.append([Link(x.text, x.get('href')) for x in _parent])
        print('%d' % 3)


    _categorys = sorted(_categorys, key=len)
    for result in _categorys[-1] : # 결과의 링크를 출력
        print('%s, %s' % (result.title, result.href))