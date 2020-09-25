# ver proto3

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

PAGE_KEY = '&page='                             # page로 추정되는 위치의 시작          
ITEM_KEY = {re.compile('.product_no=.'),        # item로 추정되는 위치의 시작
            re.compile('./goods/.')}
SOLDOUT_KEY = {'soldout', 'sellout', '품절'}
# ▼
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
    body = None
    while True :
        try :
            body = BeautifulSoup(urlopen(xurl), "html.parser").find('body') # url의 body를 반환
            break
        except :
            print('# get body error')
            continue

    return body

def get_tag(xtag, xbs, xkey) :
    return xbs.find_all(xtag, href=xkey) # href속성에 key가 존재하는 tag를 반환

def get_tag_parent(xtag, xbs, xkey) :
    tags = get_tag(xtag, xbs, xkey)

    deep_tags = list() # 검색 결과와 부모수가 저장될 dict list
    for _tag in tags :
        parent = _tag.parent
        c_parent = 0
        while str(type(parent)) == "<class 'bs4.element.Tag'>" :
            c_parent += 1
            parent = parent.parent
        deep_tags.append({'tag' : _tag, 'parent' : c_parent})

    if len(deep_tags) > 0 :
        afsdfasdf = 1

    less_tags = list() # 부모수가 적은, 높은 태그만 남긴 dict list
    for _tag in deep_tags :
        b_match = False
        temp_parent_tags = list(less_tags)
        for _cond in temp_parent_tags :
            if _tag.get('tag').get('href') == _cond.get('tag').get('href') : # 중복된 href를 가질때
                b_match = True # 중복 플래그를 True
                if _tag.get('parent') < _cond.get('parent') : # 신규 값이 보다 상위 태그일때
                    less_tags.remove(_cond)
                    less_tags.append(_tag) # 기존 값을 삭제하고 신규 값을 추가
                elif _tag.get('parent') == _cond.get('parent') : # 깊이가 같을때
                    c_next_tag, c_next_cond = 0, 0
                    for _next in _tag.get('tag').next_siblings :
                        c_next_tag += 1
                    for _next in _cond.get('tag').next_siblings :
                        c_next_cond += 1
                    if c_next_tag > c_next_cond : # 형제수가 많은 쪽을 저장
                        less_tags.remove(_cond)
                        less_tags.append(_tag) # 기존 값을 삭제하고 신규 값을 추가
                    elif c_next_tag == c_next_cond : # 형제수가 같을땐 무조건 부모를 저장
                        less_tags.remove(_cond)
                        less_tags.append({'tag' : _tag.get('tag').parent, 'parent' : -1}) # 기존 값을 삭제하고 신규 값을 추가


        if b_match == False : # 중복 결과가 없을때
            less_tags.append(_tag) # 신규 값을 추가
    return less_tags

def get_page(xurl) :
    body = get_bodytag(xurl)
    if body == None :
        return 0, 0
    page_tags = get_tag('a', body, re.compile('.' + PAGE_KEY + '.'))
    page_tags = list({x : x.get('href') for x in page_tags}.values())
    result = list()
    for _tag in page_tags :
        ex_page = _tag[_tag.find(PAGE_KEY) + 6:] # page로 추정되는 위치의 문자열 추출
        if ex_page.isdigit() : # 문자열이 숫자일때
            result.append(int(ex_page)) # 문자열을 숫자로 형변환후 저장
    return (min(result), max(result)) if len(result) > 0 else (0, 0) # 저장된 페이지 리스트 반환

def get_item(xurl, xlen) :
    body = get_bodytag(xurl)
    if body == None :
        return

    page_matchs = [body.prettify().count(x) for x in SOLDOUT_KEY] # body에서 품절키를 카운트
    if xlen != 0 and max(page_matchs) >= xlen : # 상품 최대 개수 이상일때 검색하지 않음
        return # 검색마다 최대 100개의 상품이 검색될때 100개의 품절키가 검색되면 페이지 내 모든 상품이 품절이라 가정

    items = list() # 판매 가능한 아이템 리스트
    item_tags = get_tag_parent('a', body, ITEM_KEY)
    for _tag in item_tags :
        result = _tag.get('tag').prettify() # 현재 태그 정보를 저장
        next_tag = _tag.get('tag').next_siblings # 다음 태그정보 포인트
        if next_tag != None : # 다음 태그가 존재할때
            for _next in next_tag :
                result += _next.prettify() if str(type(_next)) == "<class 'bs4.element.Tag'>" else _next # 다음 태그 정보들을 저장

        item_matchs = [result.count(x) for x in SOLDOUT_KEY]
        if max(item_matchs) == 0 :
            if _tag.get('parent') > 0 :
                items.append(_tag.get('tag').get('href'))
            else :
                a_tag = get_tag('a', _tag.get('tag'), ITEM_KEY)
                items.append(a_tag[0].get('href'))
    # for _href in  items:
    #     num_start = _href.find(ITEM_KEY) + len(ITEM_KEY) # 상품 번호 시작위치
    #     num_end = _href.find(ITEM_END_KEY, num_start) # 상품번호 종료 위치
    #     num_item = _href[num_start : num_end] # 상품번호로 추측되는 번호 추출
    #     if num_item.isdigit() and num_item not in (x for x in result) : # 추출한 상품 번호가 숫자이며, result의 원소들이 문자열을 포함하지 않을때
    #         result.append(_href) # 상품번호 중복이 없는 href만 저장
    return items
    
def get_fullitem(xshop) :
    for _cate in xshop.cates :
        cate_url = get_url(xshop.shop, _cate.get('href'))
        print('cate %s result' % _cate.get('name'))
        if 'NEW' in _cate.get('name') :
            vvvvvadsf = 123
        pages = get_page(cate_url) # i번째 카테고리에서 페이지를 불러옴
        in_page = 0

        cate_items = list() # i번째 카테고리 내 모든 페이지의 상품 url, 상품 번호 
        start_time = time.time() # 상품 검색 시간 측정
        print('\t%d ~ %d pages' % (pages))
        for page in range(pages[0], pages[-1]) : # 첫번째 페이지부터 마지막 페이지까지 탐색
            page_items = get_item(cate_url + PAGE_KEY + str(page), in_page)
            if page_items == None or len(page_items) == 0 : # 페이지에 상품이 없으면 검색을 카테고리 검색을 중지
                break
            in_page = len(page_items) if len(page_items) >= in_page else in_page
            cate_items.extend(page_items) # 아이템 탐색결과 저장
        if len(cate_items) > 0 :
            _cate['itmes'] = cate_items
        print('\t%sea, %4fsec' % (len(cate_items), time.time() - start_time))
    return

if __name__ == '__main__' :
    shop_list = list() # shop list, must started http://, ended /
    # shop_list.append(Shop("http://www.da-sara.com/"))
    # shop_list.append(Shop("http://www.swingingseoul.com/"))
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