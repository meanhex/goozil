# input = int i, j (0 < input < 1,000,000)
# output =
# 1. pirnt i, j 
# 2. pirnt max cycle len for i to j 


def cal_cycle(n) :
    cycle = 1
    strat = n
    while strat != 1:
        if strat % 2 == 0:
            strat = strat / 2
        else:
            strat = 3 * strat + 1
        cycle += 1
    
    #print('try %d, resut %d' % (n, cycle))
    return cycle

while 1 :
    #val = str(input('input 2 int : ')).split(' ')
    val = str(input()).split(' ')
    if val[0].isdigit() and val[1].isdigit() :
        val[0] = int(val[0])
        val[1] = int(val[1])
        break
    else :
        print('worng input')

_cycle = 0 # 지금까지 계산된 사이클 길이
_level = min(val) # 현재 숫자
while max(val) >= _level :
    _cycle += cal_cycle(_level)
    _level += 1

print('%d %d %d' % (val[0], val[1], _cycle))