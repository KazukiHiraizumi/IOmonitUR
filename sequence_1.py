import time
import sys

#Bit address
LAUNCH=4
FINISH=5
#Data address
PRGN=0
ENDN=1
CAPROW=20
CAPCOL=21

print('Start 1201')
setInReg(PRGN,1201)

time.sleep(0.1)
setInBit(LAUNCH,True)
while not getOutBit(LAUNCH):
  time.sleep(0.1)
setInBit(LAUNCH,False)

while not getOutBit(FINISH):
  time.sleep(0.1)

endn=getOutReg(ENDN)
if endn==100:
  print('Success')
elif int(endn/10)==92:  #solve error
  pass
elif endn==990:  #no workpiece
  pass
elif endn==802:  #bucket empty
  pass
elif endn==823:  #CV occupied
  pass
else:
  print('Error to exit')
  sys.exit()

print('End one cycle')

