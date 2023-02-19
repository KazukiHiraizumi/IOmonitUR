# One cycle auto

import time
import sys

#Bit address
LAUNCH=4
FINISH=5
#Data address
PRGN=0
ENDC=1
CAPROW=20
CAPCOL=21

#Globals
retry=0

if getInRegs(CAPCOL)==0 and getInRegs(CAPROW)==0:
  print('Bucket search PRG#1401')
  setInReg(PRGN,1401)
else:
  print('One cycle PRG#1201')
  setInReg(PRGN,1201)

while True:
  time.sleep(0.1)
  setInBit(LAUNCH,True)
  while not getOutBit(LAUNCH):
    time.sleep(0.1)
  setInBit(LAUNCH,False)
  print('Launched')
  prgn=getOutReg(PRGN)

  while not getOutBit(FINISH):
    time.sleep(0.1)
  endc=getOutReg(ENDC)

  if endc==100:
    print('Success')
    if int(prgn/100)==12: #auto cycle prgn=1200-1299
      print('Restart PRG#1201')
      setInReg(PRGN,1201)
      continue
    elif prgn==1401:
      print('Start PRG#1202')
      setInReg(PRGN,1202)
      continue
    else:
      print('Stop cycle')
      break
  elif int(endc/10)==92:  #solve error endc=920-929
    if retry<3:
      retry=retry+1
      print('Retry PRG#1203')
      setInReg(PRGN,1203)
      continue
    else:
      print('Retry counts over')
      break
  elif endc==990:  #no workpiece
    retry=0
    print('No workpiece PRG#1202')
    setInReg(PRGN,1202)
    col=getInRegs(CAPCOL)
    if col<2:
      setInRegs(CAPCOL,col+1)
    else:
      setInRegs(CAPCOL,0)
      setInRegs(CAPROW,getInRegs(CAPROW)+1)
    continue
  elif endc==802:  #bucket empty
    print('Bucket empty PRG#1001')
    setInReg(PRGN,1001)
    continue
  elif endc==823:  #CV occupied
    print('CV full')
    break
  else:
    print('Something wrong',endc)
    break

print('Stopped')

