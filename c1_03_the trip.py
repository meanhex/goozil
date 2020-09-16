# 여행
# input : 
# 1. n : 여행에 참여한 학생의 수
# 2. n개의 m : 각 학생의 지출
# 3. : 0을 입력하면 종료
# output : 각 여행에 대해 각 학생이 사용한 금액이 같아지기 위해 전달되어야 하는 금액의 총합을 출력
# 해맨이유 : 서술자료에선 '똑같아지기 위해 전달되어야 하는 최소 액수를 구하라 해놓고 output은
#            다르게 기술되어 있어 어떤 방법을 써야할지 햇갈렸음


num_stdt = 0
while True :
    read_stdt = input('input num of students : ')
    if read_stdt.isdecimal() and int(read_stdt) < 1000 :
        num_stdt = int(read_stdt)
        break
    else :
        print('worng input')

spends = list() # 금액을 담을 배열
level = 0 # 반복 단계 : 잘못된 인원수를 입력할 경우 continue 시키기 위함
while level < num_stdt : 
    read = input('%d : ' % (level + 1))
    if read.isdigit == False or float(read) > 10000 :
        print('wrong input')
        continue
    spends.append(float(read))
    level += 1

avrg = sum(spends) / num_stdt # 여행비의 평균

less_spends = [avrg - x for x in spends if x < avrg] # 조건에 맞는 값을 'avrg - x' 처리하여 복사

print(sum(less_spends))