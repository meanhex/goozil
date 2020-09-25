# 지뢰찾기
# input : 
# 1. n m
# 2. m 개의 문자를 n번 입력
# 해맨이유 : 배열의 길이로 배열을 할당하는 방법을 찾는대 오래걸림

def create_field(mine) :
    clue = [[0 for col in range(len(mine[0]))] for row in range(len(mine))]
    for y in range(len(mine)) :
        for x in range(len(mine[0])) :
            if mine[y][x] =='*' :
                print('%d %d' % (y, x))
                if x - 1 >= 0 :
                    clue[y][x - 1] += 1
                    if y - 1 >= 0 :
                        clue[y - 1][x - 1] += 1
                    if y + 1 < len(mine) :
                        clue[y + 1][x - 1] += 1
                if x + 1 < len(mine[0]) :
                    clue[y][x + 1] += 1
                    if y - 1 >= 0 :
                        clue[y - 1][x + 1] += 1
                    if y + 1 < len(mine) :
                        clue[y + 1][x + 1] += 1
                if y - 1 >= 0 :
                    clue[y - 1][x] += 1
                if y + 1 < len(mine) :
                    clue[y + 1][x] += 1
    return clue

while 1 :
    val = str(input()).split(' ')
    if val[0].isdigit() and val[1].isdigit() :
        val[0] = int(val[0])
        val[1] = int(val[1])
        break
    else :
        print('worng input')

level = 0
mine = [[0 for col in range(val[1])] for row in range(val[0])]

while level < val[0] :
    line = str(input('%d : ' % level))
    if len(line) == val[1] :
        mine[level] = line
        level += 1
    else :
        print('worng input')

clue = create_field(mine)
for y in clue :
    print(y)