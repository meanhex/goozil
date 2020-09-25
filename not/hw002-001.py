import time

print("안녕")
x = 0
while True:
    if x < 6:
        x = x+1
        print(x)
        time.sleep(1)
    else:
        print("끝")
        break