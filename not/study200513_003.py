# study
import sys

print ("-----------------------------------------")
print ("In/Output device study")
print ("-----------------------------------------")

userInput = input ('입력후 엔터키를 누르세요 : ')
print ("입력한 %s는 %s입니다." % ("문자열" if len(userInput) > 1 else "문자", userInput))
