# ver proto3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

PAGE_KEY = '&page='             # page로 추정되는 위치의 시작
ITEM_KEY = 'product_no='        # item로 추정되는 위치의 시작
ITEM_END_KEY = '&'              # item로 추정되는 위치의 끝
# ▼

# ▼target class
# class Link :
#     def __init__(self, title, href) :
#         super().__init__()
#         self.title = title
#         self.href = href
#     def __setitem__(self, title, href) :
#         self.title = title
#         self.href = href

class Shop :
    def __init__(self, shop) :
        super().__init__()
        self.shop = shop
        self.title = ''
        self.cates = list()
    def setCates(self, cates) :
        self.cates = cates
    def getCates(self) :
        return self.cates
    # def getCate(self,_index) :
    #     if _index >= len(self.cates) :
    #         return None
    #     if 'http://' in self.cates[_index].href or 'https://' in self.cates[_index].href :
    #         return self.cates[_index].href
    #     return self.shop + self.cates[_index].href
    def show(self) :
        print('#%s' % self.title)
        for _cate in self.cates : 
            print('\t%-20s : %s' % (_cate.get('name'), _cate.get('href')))

def get_url(xshop_url, xurl) :
    if '&' in xurl : 
        xurl = xurl.split('&')[0]
    if 'http://' in xurl or 'https://' in xurl :
        return xurl
    else :
        return xshop_url + xurl

# ▼ shop_list, tag_keys, cate_keys를 인자로 shop의 카테로리로 추정되는 link목록을 추가한 shop_list를 반환
def get_cate(xshop, xtag_keys, xcate_keys) :
    bs = BeautifulSoup(urlopen(xshop.shop), "html.parser")
    xshop.title = bs.head.title.string
    body = bs.find('body')
    cates = list()
    href_results = list() # result for tag with href
    
    # 검색 시작
    href_results = body.find_all(xtag_keys, href=xcate_keys) # search to tag with href
    for result in href_results :
        if len(result.text) > 2 : # 검색 결과중 '\n\n'도 포함되어 조건에 추가
            cates.append({'name' : result.text.replace('\n', ''), 'href' : result.get('href'), 'items' : None})
        elif 'alt' in result.attrs and len(result.attrs['alt']) > 2 :
            cates.append({'name' : result.attrs['alt'].replace('\n', ''), 'href' : result.get('href'), 'items' : None})
        elif result.next != None and type(result) == type(result.next) : #
            if len(result.next.text) > 2 :
                cates.append({'name' : result.next.text.replace('\n', ''), 'href' : result.get('href'), 'items' : None})
            elif 'alt' in result.next.attrs and len(result.next.attrs['alt']) > 0 :
                cates.append({'name' : result.next.attrs['alt'].replace('\n', ''), 'href' : result.get('href'), 'items' : None})
    # 검색 완료
    if len(cates) > 2 : # 검색결과가 2개 이상 있을때
        cates = list({x.get('href') : x for x in cates}.values()) # href 기준으로 중복을 제거
        xshop.setCates(cates) # for문으로 가져온 현재 xshop의 cates에 저장
    else : 
        print('cate length is short than 3') # 검색 결과가 1개 이하일땐 저장하지 않음 : 카테고리가 1개 이하인 쇼핑몰은 없다고 가정
    return

def get_bodytag(xurl) :
    return BeautifulSoup(urlopen(xurl), "html.parser").find('body') # url의 body를 반환

def get_href(xbs, xkey) :
    href_results = xbs.find_all('a', href=xkey) # href속성에 key가 존재하는 'a' tag를 검색함
    hrefs = [x.get('href') for x in href_results] # href만 추출
    hrefs = list({x : x for x in hrefs}.values()) # 중복 제거
    return hrefs

def get_href_parent(xbs, xkey, conds) :
    href_results = xbs.find_all('a', href=xkey) # href속성에 key가 존재하는 'a' tag를 검색함

    parent_hrefs = list() # 검색 결과와 부모수가 저장될 dict list
    for _href in href_results :
        href_parent = _href.parent
        c_parent = 0
        while href_parent != None :
            c_parent += 1
            href_parent = href_parent.parent
        parent_hrefs.append({'result' : _href, 'parent' : c_parent})

    if len(parent_hrefs) > 0 :
        afsdfasdf = 1
    

    cond_hrefs = list() # 부모수와 비교해 중복 제거한 dict list
    for _href in parent_hrefs :
        b_match = False
        _temp_cond_hrefs = list(cond_hrefs)
        for _cond in _temp_cond_hrefs :
            if _href.get('result').get('href') == _cond.get('result').get('href') :
                b_match = True
                if _href.get('parent') < _cond.get('parent') :
                    cond_hrefs.remove(_cond)
                    cond_hrefs.append(_href)
        if b_match == False :
            cond_hrefs.append(_href)

    hrefs = list()
    for _href in cond_hrefs :
        result = _href.get('result').prettify()
        href_next = _href.get('result').next_siblings
        if href_next != None :
            for _next in href_next :
                vbasdf = 1
                result += _next.prettify() if str(type(_next)) == "<class 'bs4.element.Tag'>" else _next
        # while href_next != None and str(type(href_next)) == "<class 'bs4.element.Tag'>":
        #     result += href_next.prettify()
        #     href_next = href_next.next_sibling

        cnods_match = [result.count(x) for x in conds]
        if max(cnods_match) == 0 :
            hrefs.append(_href.get('result').get('href'))
    
    #hrefs = [x.get('href') for x in href_results] # href만 추출
    hrefs = list({x : x for x in hrefs}.values()) # 중복 제거
    return hrefs

def get_page(xurl) :
    body = get_bodytag(xurl)
    page_href = get_href(body, re.compile('.' + PAGE_KEY + '.'))
    result = list()
    for x in page_href :
        ex_page = x[x.find(PAGE_KEY) + 6:] # page로 추정되는 위치의 문자열 추출
        if ex_page.isdigit() : # 문자열이 숫자일때
            result.append(int(ex_page)) # 문자열을 숫자로 형변환후 저장
    return result # 저장된 페이지 리스트 반환

def get_item(xurl, xlen) :
    # 페이지 상품수가 가장 많이 담길때만 xlen 갱신.
    # 품절이 xlen과 같으면 스킵
    result = list()
    conds = {'soldout', 'sellout', '품절'}
    body = get_bodytag(xurl)

    cnods_match = [body.prettify().count(x) for x in conds]
    if xlen != 0 and max(cnods_match) >= xlen :
        return result

    item_href = get_href_parent(body, re.compile('.' + ITEM_KEY + '.'), conds)

    for _item in  item_href:
        num_start = _item.find(ITEM_KEY) + len(ITEM_KEY) # 상품 번호 시작위치
        num_end = _item.find(ITEM_END_KEY, num_start) # 상품번호 종료 위치
        num_item = _item[num_start : num_end] # 상품번호로 추측되는 번호 추출
        if num_item.isdigit() and num_item not in (x for x in result) : # 추출한 상품 번호가 숫자이며, result의 원소들이 문자열을 포함하지 않을때
            result.append(_item) # 상품번호 중복이 없는 href만 저장
    return result
    
def get_fullitem(xshop) :
    for _cate in xshop.cates :
        cate_url = get_url(xshop.shop, _cate.get('href'))
        print('cate %s result' % _cate.get('name'))
        if 'NEW' in _cate.get('name') :
            vvvvvadsf = 123
        pages = get_page(cate_url) # i번째 카테고리에서 페이지를 불러옴
        in_page = 0
        if len(pages) > 0 : 
            cate_items = list() # i번째 카테고리 내 모든 페이지의 상품 url, 상품 번호 
            print('\t%d ~ %d pages' % (min(pages), max(pages)))
            for page in range(min(pages), max(pages)) : # 첫번째 페이지부터 마지막 페이지까지 탐색
                page_items = get_item(cate_url + PAGE_KEY + str(page), in_page)
                if len(page_items) == 0 : # 페이지에 상품이 없으면 검색을 카테고리 검색을 중지
                    break
                in_page = len(page_items) if len(page_items) >= in_page else in_page
                cate_items.extend(page_items) # 아이템 탐색결과 저장
            if len(cate_items) > 0 :
                _cate['itmes'] = cate_items
            print('\t%sea' % len(cate_items))
    return

if __name__ == '__main__' :
    shop_list = list() # shop list, must started http://, ended /
    shop_list.append(Shop("http://www.da-sara.com/"))
    shop_list.append(Shop("http://www.swingingseoul.com/"))
    shop_list.append(Shop("http://www.smoothie-star.com/"))
    shop_list.append(Shop("http://www.melodystyle.co.kr/"))
    shop_list.append(Shop("http://www.drvtg.co.kr/")) # 카테고리에 브랜드 카테고리까지 있음
    shop_list.append(Shop("http://gujenara.co.kr/")) # 주석이나 카테고리 텍스트 없이 이미지로만 된 사이트
    shop_list.append(Shop("http://regarment.com/"))

    tag_keys = list() # tag keyword list : tag for category
    tag_keys.append('a')
    tag_keys.append('img')

    cate_words = list() # category keyword list : category for used item
    cate_words.append(r'.list[.]+\w+[?].') # ~list.□?~
    cate_keys = [re.compile(x) for x in cate_words] # 정규식 추가

    
    
    for _shop in shop_list :
        get_cate(_shop, tag_keys, cate_keys)
        _shop.show()
        get_fullitem(_shop)
    
    print('done')