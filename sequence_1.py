# Home

import time
import sys

#Bit address
LAUNCH=4
FINISH=5
#Data address
PRGN=0
ENDN=1

print('Start 1001')
setInReg(PRGN,1001)

time.sleep(0.1)
setInBit(LAUNCH,True)
while not getOutBit(LAUNCH):
  time.sleep(0.1)
setInBit(LAUNCH,False)

