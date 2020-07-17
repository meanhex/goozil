00#
# import math
# import copy
# a = [5,2,9,4,1]
# b = copy.deepcopy(a)
#
# b[2] = 8
#
# a.append(6)
# a.insert(0, 0)
# a.sort()
# a.reverse()
# c = min(a)
# d = max(a)
# print(c, d)
# print(a)
# print(b)
#
#
#
# # a의 0번째 index  와 b의 2번째 index 더하기
#
# wa = a[0]
# wb = b[2]
# print( wa + wb)
#
# # a의 0번째 index  와 b의 2번째 index 평균값
# print( (a[0]+b[2])/2)
#
# # a의 0번째 index  와 b의 2번째 index 나눈 몫과 나머지 출력
# wc =(a[0] // b[2])
# wd =(a[0] % b[2])
# print("몫은 %d 나머지는 %d " % (wc,wd))
#
# # pow 제곱  abs() 절대값 round() 반올림 round(a,b) b 아래 반올림  + 형변환
#
# print( "%d" %abs(-5))
# print( "%f" %round(5.6234123344))
# print( "%f" %round(5.62361234,7))
#
# q = float(input("숫자입력 : "))
# waa = (pow(q,2))
# print(waa)
#
# print(type(q))
#
# # math.sqrt 제곱근
# # sin() 싸인 cos () 코싸인 tan () 탄젠트 a~ ~역
# wbb = math.sqrt(waa)
# print(int(wbb))
#
# 1. 3.141592의 값을 소숫점 4자까지 표현되도록 반올림후 표시 하시오.
# 2. 사용자에게 입력받은 수의 평균을 구하는 프로그램을 작성하시오. (x키를 통해 입력을 종료받고, 그전까지는 숫자를 계속 입력 받도록 작성)


# sum = 0
# c=1
# while True:
#     b =  input("%d 번째 값을 입력 하시오 " %c)
#     if b.isdigit():
#         sum += int(b)
#         print(sum)
#         c = c+1
#     elif b == "x":
#         print("%d번째 까지의 평균값은 %f 입니다." %(c ,(sum/c)))
# 
#         break
#     else :
#         print("입력값이 잘못되었습니다.")
# 문자나누기 C = A.sprit(B)
# 문자 찾기  C = A.find(B) C 는  A안에 B가 있는 인덱스 순번 출력
# 카운트 하기  C = A.count(B) A문자열에서 B문자열 발생횟수 리턴
#                
#                
# #                A="Abcdef" ㄴ#                 >>>pirnt(A.upper())
#                 ABCDEF
#                 print(A.lower())- 소문자
# #                 print(A.swapcase())-대소문자 반전
# a배열 요소를 b문자열로 구분하여 나눠 c에 저장c = a.split(b)
# a문자열에서 b문자열을 검색후 인덱스를 반환 a.find(b)
# a문자열에서 b문자 발생횟수 리턴a.count(b)
# a.uppper() 대문자로
# a.lower() 소문자로
# a.swapcase() 대소문자 반전
# a문자열이 b문자열로 시작하는가 a.startswith(b)
# a문자열의 c인덱스가 b문자열로 시작하는가 a.startswith(b, c)
# a문자열의 c인덱스부터 d인덱스까지가 b문자열로 끝나는가 b.endwith(b, c, d)
# a문자열 길이가 b가될때까지 앞에 0을 채움 a.zfill(b)
# a문자열 길이가 b가될때까지 앞에 c문자열을 채움 a.zfill(b, c)
# a.isalpha() 문자열이 문자여부 참거짓 반환
# a.isdigit() 문자열이 숫자여부 참거짓 반환
# - 문자열 처리설명
#
# 1. 문자열 '3.14'값을 형변환 하여 소숫점자리 없이 반올림 한후 2을 더하시오. 그 후 최대길이가 3이되는 형식으로 0을 채워 표시 하시오.
# 2. 입력받은 문자열을 한글자씩 표시하시오.