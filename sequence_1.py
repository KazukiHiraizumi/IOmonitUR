import time

print('Start sequence')
setIntReg(0,300)
time.sleep(3)
setBitReg(3,True)
time.sleep(3)
setBitReg(3,False)
print('End sequence')

