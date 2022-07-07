import time
import eventlet#导入eventlet

def say():
    time.sleep(3)
    print('1')

eventlet.monkey_patch()#引入patch
with eventlet.Timeout(2,False):#设置超时时间为2秒
    say()
print('2')