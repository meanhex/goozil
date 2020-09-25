# ver proto5
# 상하단에서 상품을 추가로 표시하는 사이트는 제외
# 카테고리가 주석없이 이미지로만 표시되는 경우 제외
# tag search :      1. 파라메터 KEY를 포함하는 href를 가진 a tag를 검색
#                   2. 중복이 발생할 경우, 깊이가 보다 상위 태그(부모로부터 가까운) 태그를 선택
#                   3. 깊이가 같을 경우, 보다 많은 형제를 가진 태그를 선택
#                   4. 형제가 같을 경우, 부모태그를 선택한 후 깊이를 -1로 표시
# catagory search : 1. 태그 자체 정보 -> 자식 태그 정보 -> 형제 태그 정보 순으로 검색
# page search :     1. 카테고리 url로 접근
#                   2. PAGE_KEY와 매치되는 a tag를 모두 수집
#                   3. tag내 href속성의 특정 지점을 추출
#                   4. min page ~ max page로 설정함
# item search :     1. 카테고리에서 검색된 page url으로 접근,
#                   2. ITEM_KEY와 매치되는 a tag를 모두 수집,
#                   3. tag의 자식, 형제 모두중 SOLDOUT_KEY를 포함하는 경우 수집 안함

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time

CATE_KEY = {re.compile(r'.list[.]+\w+[?].'),    #
            }
TAG_KEY = {'a', 'img'}                          # 
PAGE_KEY = '&page='                             # page로 추정되는 위치의 시작          
ITEM_KEY = {re.compile('.product_no=.'),        # item로 추정되는 위치의 시작
            re.compile('./goods/.'),
            re.compile('.[?]index_no=.')}
SOLDOUT_KEY = {'soldout', 'sellout', '품절'}
# ▼
class Shop :
    def __init__(self, url) :
        super().__init__()
        self.url = url
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

def get_bodytag(xurl) :
    body = None
    while True :
        try :
            body = BeautifulSoup(urlopen(xurl), "html.parser").find('body') # url의 body를 반환
            if body != None :
                break
            else :
                print('# get body error')
        except :
            print('# get body error')
            continue

    return body

def get_tag(xtag, xbs, xkey) :
    return xbs.find_all(xtag, href=xkey) # href속성에 key가 존재하는 tag를 반환

def get_tag_deep(xtag, xbs, xkey) :   # dict{'tag' : 검색된 tag정보, 'deep' : 깊이 정보}
                                        # (deep : -1    = 최종 예외되어 부모가 저장됨)
                                        # (deep : 0     = 중복이 없어 깊이 정보가 필요없는 tag)
    tags = get_tag(xtag, xbs, xkey)
    only_hrefs = list({x : x.get('href') for x in tags}.values()) # tag 속성중 href가 중복되지 않은 href값을 저장

    if len(tags) == len(only_hrefs) : # 단순 href 중복 제외된 리스트가 같다면 deep 분류 처리 없이 deep : 0으로 반환한다.
        return [{'tag' : x, 'deep' : 0} for x in tags]
        # deep 분류가 필요없는 리스트는 처리 안하기 위함

    # deep 분류 처리를 통해 중복결과중 보다 유효한 tag list를 저장함
    deep_tags = list() # deep, tag가 단순 저장될 list
    for _tag in tags :
        parent = _tag.parent
        c_parent = 0
        while str(type(parent)) == "<class 'bs4.element.Tag'>" :
            c_parent += 1
            parent = parent.parent
        deep_tags.append({'tag' : _tag, 'deep' : c_parent})

    less_tags = list() # 중복된 tag중(0) deep가 낮은 값(1), 같다면 많은 next(2), 같다면 부모를 저장함(3)
    for _tag in deep_tags :
        b_match = False
        temp_parent_tags = list(less_tags)
        for _cond in temp_parent_tags :
            if _tag.get('tag').get('href') == _cond.get('tag').get('href') : # (0)중복된 href를 가질때
                b_match = True # 중복 플래그를 True
                if _tag.get('deep') < _cond.get('deep') : # (1)deep가 낮을때
                    less_tags.remove(_cond)
                    less_tags.append(_tag) # 기존 값을 삭제하고 신규 값을 추가
                elif _tag.get('deep') == _cond.get('deep') : # (1)의 예외
                    c_next_tag, c_next_cond = 0, 0 # next 갯수를 카운트
                    for _next in _tag.get('tag').next_siblings : c_next_tag += 1
                    for _next in _cond.get('tag').next_siblings : c_next_cond += 1

                    if c_next_tag > c_next_cond : # (2)많은 next를 가질때
                        less_tags.remove(_cond)
                        less_tags.append(_tag) # 기존 값을 삭제하고 신규 값을 추가
                    elif c_next_tag == c_next_cond : # (2)의 예외 (3)부모를 저장함
                        less_tags.remove(_cond)
                        less_tags.append({'tag' : _tag.get('tag').parent, 'deep' : -1}) # 기존 값을 삭제하고 신규 값을 추가

        if b_match == False : # 중복 결과가 없을때
            less_tags.append(_tag) # 신규 값을 추가
    return less_tags

def get_page(xurl) :
    body = get_bodytag(xurl)
    page_tags = get_tag('a', body, re.compile('.' + PAGE_KEY + '.'))
    page_tags = list({x : x.get('href') for x in page_tags}.values()) # tag 속성중 href가 중복되지 않은 href값을 저장
    result = list()
    for _tag in page_tags :
        ex_page = _tag[_tag.find(PAGE_KEY) + 6:] # page로 추정되는 위치의 문자열 추출
        if ex_page.isdigit() : # 문자열이 숫자일때
            result.append(int(ex_page)) # 문자열을 숫자로 형변환후 저장
    return (min(result), max(result)) if len(result) > 0 else (0, 0) # 저장된 페이지 리스트 반환

def get_item(xurl, xlen) :
    body = get_bodytag(xurl)

    page_matchs = [body.prettify().count(x) for x in SOLDOUT_KEY] # body에서 품절키를 카운트
    if xlen != 0 and max(page_matchs) >= xlen : # 상품 최대 개수 이상일때 검색하지 않음
        return # 검색마다 최대 100개의 상품이 검색될때 100개의 품절키가 검색되면 페이지 내 모든 상품이 품절이라 가정

    items = list() # 판매 가능한 아이템 리스트
    item_tags = get_tag_deep('a', body, ITEM_KEY)
    for _tag in item_tags :
        result = _tag.get('tag').prettify() # 현재 태그 정보를 저장
        next_tag = _tag.get('tag').next_siblings # 다음 태그정보 포인트
        if next_tag != None : # 다음 태그가 존재할때
            for _next in next_tag :
                result += _next.prettify() if str(type(_next)) == "<class 'bs4.element.Tag'>" else _next # 다음 태그 정보들을 저장

        item_matchs = [result.count(x) for x in SOLDOUT_KEY] # 같은 deep의 tag에서 SOLDOUT 검색
        if max(item_matchs) == 0 : # SOLDOUT이 아닐때
            if _tag.get('deep') >= 0 : # deep가 일반 일때
                items.append(_tag.get('tag').get('href'))
            else : # deep가 부모를 가르킬때
                items.append(_tag.get('tag').find('a').get('href'))
                # deep = -1 은 중복 tag들 중에서 보다 유효한 tag를 가리지 못한 경우임
                # 따라서 부모에서 검색된 자식 a tag중 어느 tag를 가져와도 된다고 가정

    # for _href in  items:
    #     num_start = _href.find(ITEM_KEY) + len(ITEM_KEY) # 상품 번호 시작위치
    #     num_end = _href.find(ITEM_END_KEY, num_start) # 상품번호 종료 위치
    #     num_item = _href[num_start : num_end] # 상품번호로 추측되는 번호 추출
    #     if num_item.isdigit() and num_item not in (x for x in result) : # 추출한 상품 번호가 숫자이며, result의 원소들이 문자열을 포함하지 않을때
    #         result.append(_href) # 상품번호 중복이 없는 href만 저장
    return items

# ▼ shop_list, tag_keys, cate_keys를 인자로 shop의 카테로리로 추정되는 link목록을 추가한 shop_list를 반환
def start_search_cate(xshop) :
    bs = BeautifulSoup(urlopen(xshop.url), "html.parser")
    body = bs.find('body')
    xshop.title = bs.head.title.string # shop class에 title 등록

    cates = list()
    cate_tags = get_tag_deep(TAG_KEY, body, CATE_KEY)
    for _tag in cate_tags : # tag 속성에 text가 있는 경우(0), alt 속성이 있을 경우(1), (2), 같다면 부모를 저장함(3)
        if _tag.get('deep') < 0 :
            _tag['tag'] = _tag.get('tag').find('a')
        select_href = _tag.get('tag').get('href') # 저장할 href
        if '&sort' in select_href : # href에 불필요한 옵션이 있을때
            select_href =  select_href.split('&sort')[0] # 옵션 제거

        select_name = '' # 저장할 cate name
        if len(_tag.get('tag').text.replace('\n', '')) > 0: # (0)
            select_name = _tag.get('tag').text.replace('\n', '')
        elif 'alt' in _tag.get('tag').attrs and len(_tag.get('tag').attrs.get('alt').replace('\n', '')) > 0 : # (1)
            select_name = _tag.get('tag').attrs.get('alt').replace('\n', '')
        else : # cate name을 찾을 수 없을때 
            for _child in _tag.get('tag').children : # 자식 검색
                    if str(type(_child)) == "<class 'bs4.element.Tag'>" :
                        if len(_child.text.replace('\n', '')) > 0 : 
                            select_name = _child.text.replace('\n', '')
                            break
                        elif 'alt' in _child.attrs and len(_child.attrs.get('alt').replace('\n', '')) > 0 : 
                            select_name = _child.attrs.get('alt').replace('\n', '')
                            break

            if len(select_name) == 0 : # 자식 검색 결과가 없을때
                for _next in _tag.get('tag').next_siblings : # 형제 검색
                    if str(type(_next)) == "<class 'bs4.element.Tag'>" :
                        if len(_next.text.replace('\n', '')) > 0 : 
                            select_name = _next.text.replace('\n', '')
                            break
                        elif 'alt' in _next.attrs and len(_next.attrs.get('alt').replace('\n', '')) > 0 : 
                            select_name = len(_next.attrs.get('alt').replace('\n', '')) > 0
                            break
                

        if len(select_name) > 0 and len(select_href) > 0 :
            cates.append({'name' : select_name, 'href' : select_href, 'items' : None})
    xshop.setCates(cates)
    return
    
def start_search_item(xshop) :
    for _cate in xshop.cates :
        cate_url = get_url(xshop.url, _cate.get('href'))
        print('cate %s result' % _cate.get('name'))
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
            _cate['items'] = cate_items
        print('\t%sea, %4fsec' % (len(cate_items), time.time() - start_time))
    return

if __name__ == '__main__' :
    shop_list = list() # shop list, must started http://, ended /
    shop_list.append(Shop("http://www.da-sara.com/"))
    shop_list.append(Shop("http://www.swingingseoul.com/"))
    shop_list.append(Shop("http://www.smoothie-star.com/"))
    # shop_list.append(Shop("http://www.melodystyle.co.kr/")) # 개같네. 페이지마다 광고 상품 존나 띄워놔서 분간하기 어려움. 좆같게 브랜드관 따로 쳐 차려놓는것도 맘에안들어 썅
    shop_list.append(Shop("http://www.drvtg.co.kr/")) # 카테고리에 브랜드 카테고리까지 있음
    # shop_list.append(Shop("http://gujenara.co.kr/")) # 주석이나 카테고리 텍스트 없이 이미지로만 된 사이트
    
    for _shop in shop_list :
        start_search_cate(_shop)
        _shop.show()
        start_search_item(_shop)
    
    print('done')