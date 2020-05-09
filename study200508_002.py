# study
import sys
import glob
import serial
import time

FIX_BAUDRATE = 9600
msgInit = '>HELL_LOW_SERIAL_PROD_0001'
print ("-----------------------------------------")
print ("Serial communocation study")
print ("-----------------------------------------")

# func. 플랫폼별 가용 시리얼 포트 검색 함수
# ref. http://blog.naver.com/PostView.nhn?blogId=msyang59&logNo=220632092938
def get_serialPort():
    # OS Platform별로 Serial port 처리
    if sys.platform.startswith('win'):
        _ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux'):
        _ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        _ports = glob.glob('dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    _reslut = [] # 반환할 port 배열
    for _port in _ports:
        try:
            _ser = serial.Serial(_port) # 임시 serial 선언
            _ser.close() # 임시 serial에 매소드를 통해 가용한 serial port 확인
            _reslut.append(_port) # exception 없이 통과하면 port 배열에 추가
        except (OSError, serial.SerialException):
            pass # exception 발생시 pass
    del(_ser)
    return _reslut

ports = get_serialPort()
if len(ports) > 0:
    resultFind = False
    for port in ports:
        print ("check available port :%s" % port)
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = FIX_BAUDRATE
        msgReadInit = ''
        timeStart = time.time()
        ser.open()
        while True:
            if ser.inWaiting() > 0:
                msgReadInit += ser.read()
            if msgReadInit in msgInit:
                resultFind = True
                break
            elif time.time() > timeStart + 5:
                breakd
            else:
                pass
            time.sleep(1)
        if resultFind:
            print ("success")
            break
        else:
            pirnt ("fail")
            ser.close()
    if resultFind == False:
        print("cant find available device")

else:
    print("there is no available port")