#!/usr/bin/env python

import PySimpleGUI as sg
import sys
sys.path.append('.')

###Outlooking #####################
import layout_simple as layout
#import layout_readonly as layout

indices=[
  '0','1','2','3','4','5','6','7','8','9',
  '10','11','12','13','14','15','16','17','18','19',
  '20','21','22','23','24','25','26','27','28','29',
  '30','31','32','33','34','35','36','37','38','39',
  '40','41','42','43','44','45','46','47'
]
contents=layout.build(indices)

window=sg.Window('I/O Monitor for UR', contents,finalize=True)

uplink=False
for k in indices:
  if '-v'+k in window.AllKeysDict:
    window['-v'+k].bind('<Return>', '')   #attach event to the widget whose key begins with '-v*'
    uplink=True
for k in indices:
  if '-u'+k in window.AllKeysDict:
#    window['-u'+k].bind('<ButtonPress-1>', '')   #attach event to the widget whose key begins with '-u*'
    uplink=True

#while True:
#  event, values = window.read()
#  sys.exit()

###RTDE connect################
import comm
IPADDS="127.0.0.1"
#IPADDS="192.168.2.100"
PORT=30004
RECIPE="minimum.xml"

if not comm.connect(IPADDS,PORT,RECIPE,uplink=uplink):
  print("comm connect falied")
  sys.exit()

###Define R/W methods##############
sendQueue=False
def setInReg(adds,val):
  global sendQueue
  k=str(adds)
  v=str(val)
  exec('comm.inregs.input_int_register_'+k+'='+v)   #set int register
  sendQueue=True
def getInReg(adds):
  return eval('comm.state.input_int_register_'+str(adds))
def getOutReg(adds):
  return eval('comm.state.output_int_register_'+str(adds))
def setInBit(adds,val):
  global sendQueue
  print('setInBit',adds,val)
  if val:
    v=comm.inregs.input_bit_registers0_to_31 | (1<<int(adds))
  else:
    v=comm.inregs.input_bit_registers0_to_31 & ~(1<<int(adds))
  comm.inregs.input_bit_registers0_to_31=v
  sendQueue=True
def getInBit(adds):
  return bool(comm.state.input_bit_registers0_to_31 & (1<<int(adds)))
sysExitRaiser=False
def getOutBit(adds):
  global sysExitRaiser
  if sysExitRaiser:
    sysExitRaiser=False
    raise SystemExit('System Exit in "getOutBit"')
  return bool(comm.state.output_bit_registers0_to_31 & (1<<int(adds)))

###Define Sequence manager##############
import threading
sequence=None
def start_sequence(n):
  global sequence
  if sequence is not None:
    if sequence.is_alive():
      print('Thread busy(running)')
      return
  print('Start sequence',n)
  try:
    sequence=threading.Thread(target=lambda : exec(open('sequence_'+str(n)+'.py').read(), globals()))
    sequence.start()
  except Exception as e:
    sequence=None
    print(e)
def stop_sequence():
  global sequence,sysExitRaiser
  if sequence is None: return
  if sequence.is_alive():
    print('Stop only has an effect in "getOutBit" method')
    sysExitRaiser=True

###Start comm##############
if not comm.start():
  print("comm start falied")
  sys.exit()

###Init Register##############
for k in indices:
  try:
    v=getInReg(k)
    setInReg(k,v)
    window['-v'+k].update(value=v)
  except Exception as e:
    print('warn init inregs',k,e)
    break
try:
  comm.inregs.input_bit_registers0_to_31=comm.state.input_bit_registers0_to_31
except Exception as e:
  print('warn init inregs',k,e)

###Start Event Loop##############
while True:
  event, values = window.read(timeout=100,timeout_key='-timeout-')

  if event == sg.WIN_CLOSED:
    print('exit')
    break

  if event.startswith('-t'): 
    if not comm.receive():
      print('receive failed')
      break
    window['robot_mode'].update(comm.state.robot_mode)
    window['runtime_state'].update(comm.state.runtime_state)
  # update integer output widget
    for k in indices:
      try:
        val=eval('comm.state.output_int_register_'+k)
      except Exception as e:
        break
      if '-o'+k in window.AllKeysDict:
        window['-o'+k].update(value=val)
  # update integer input widget
    for k in indices:
      try:
        val=eval('comm.state.input_int_register_'+k)
      except Exception as e:
        break
      if '-i'+k in window.AllKeysDict:
        window['-i'+k].update(value=val)
  # update bit output widget
    val=comm.state.output_bit_registers0_to_31
    for n,k in enumerate(indices):
      if '-y'+k in window.AllKeysDict:
        window['-y'+k].update(background_color='yellow' if val&(1<<n) else 'black')
  # update bit input widget
    val=comm.state.input_bit_registers0_to_31
    for n,k in enumerate(indices):
      if '-x'+k in window.AllKeysDict:
        window['-x'+k].update(background_color='yellow' if val&(1<<n) else 'black')
  # update sequence executer
    if sequence is None:
      if '-s0' in window.AllKeysDict: window['-s0'].update(button_color='black')
    elif sequence.is_alive():
      window['-s0'].update(button_color='red')
    else:
      window['-s0'].update(button_color='black')
      sysExitRaiser=False
  elif event.startswith('-v'):
    print('reg',event[:4],values[event[:4]])
    exec('comm.inregs.input_int_register_'+event[2:]+'='+values[event[:4]])
    sendQueue=True
  elif event.startswith('-u'):
    print('bit',event[:4])
    comm.inregs.input_bit_registers0_to_31=comm.state.input_bit_registers0_to_31^(1<<int(event[2:]))
    sendQueue=True
  elif event.startswith('-s'):
    n=int(event[2:])
    if n==0:
      stop_sequence()
    else:
      start_sequence(n)

  if sendQueue:
    comm.send()
    sendQueue=False

stop_sequence()
comm.pause()
comm.disconnect()
window.close()

