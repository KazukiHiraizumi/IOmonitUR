#!/usr/bin/env python

import PySimpleGUI as sg
import sys
sys.path.append('.')

### Outlooking #####################
import layout_simple as layout
indices=[
  '0','1','2','3','4','5','6','7','8','9',
  '10','11','12','13','14','15','16','17','18','19',
  '20','21','22','23','24','25','26','27','28','29',
  '30','31','32','33','34','35','36','37','38','39',
  '40','41','42','43','44','45','46','47'
]
contents=layout.build(indices)
seq_column=[
  [sg.Button('Sequence1'),sg.Button('Sequence2'),sg.Button('Sequence3')],
  [sg.Button('Stop')]
]
contents.append([sg.Column(seq_column,element_justification='center')])
window = sg.Window('I/O Monitor for UR', contents,finalize=True)

for k in indices:
  if '-i'+k in window.AllKeysDict:
    window['-i'+k].bind('<Return>', '')   #attach event to the widget whose key begins with '-i*'
for k in indices:
  if '-x'+k in window.AllKeysDict:
    window['-x'+k].bind('<ButtonPress-1>', '')   #attach event to the widget whose key begins with '-x*'

###RTDE connect################
import comm
IPADDS="127.0.0.1"
PORT=30004
RECIPE="minimum.xml"

if not comm.connect(IPADDS,PORT,RECIPE):
  print("comm connect falied")
  sys.exit()

###Define R/W methods##############
def setInReg(adds,val):
  k=str(adds)
  v=str(val)
  exec('comm.inregs.input_int_register_'+k+'='+v)   #set int register
  window['-i'+k].update(value=v)                    #and its corresponding widget
def getInReg(adds):
  return eval('comm.state.input_int_register_'+str(adds))
def getOutReg(adds):
  return eval('comm.state.output_int_register_'+str(adds))
def setInBit(adds,val):
  if val:
    v=comm.inregs.input_bit_registers0_to_31 | (1<<int(adds))
  else:
    v=comm.inregs.input_bit_registers0_to_31 & ~(1<<int(adds))
  comm.inregs.input_bit_registers0_to_31=v
  wkey='-x'+str(adds)
  if wkey in window.AllKeysDict:
    window[wkey].update(value=val)
  else:
    raise KeyError('Key error at',wkey)

def getInBit(adds):
  return bool(comm.state.input_bit_registers0_to_31 & (1<<int(adds)))
getOutBitRaiser=False
def getOutBit(adds):
  global getOutBitRaiser
  if getOutBitRaiser:
    getOutBitRaiser=False
    raise SystemExit('System Exit in "getOutBit"')
  return bool(comm.state.output_bit_registers0_to_31 & (1<<int(adds)))

###Define Sequence manager##############
import threading
thread=None
def do_sequence(n):
  global thread
  if thread is not None:
    if thread.is_alive():
      print('Thread busy(running)')
      return
  print('Do sequence',n)
  with open('sequence_1.py', 'r') as f:
    code=f.read()
    f.close()
    thread=threading.Thread(target=lambda : exec(code))
    thread.start()
def stop_sequence():
  global thread,getOutBitRaiser
  if thread is None: return
  if thread.is_alive():
    print('Stop only has an effect in "getOutBit" method')
    getOutBitRaiser=True

###Start comm##############
if not comm.start():
  print("comm start falied")
  sys.exit()

###Init Register##############
for k in indices:
  try:
    setInReg(k,getInReg(k))
  except Exception as e:
    print('error in reg',k,e)
    break

comm.inregs.input_bit_registers0_to_31=0
for k in indices:
  try:
    setInBit(k,getInBit(k))
  except Exception as e:
    print('error in bit',k,e)
    break

###Start Event Loop##############
while True:
  event, values = window.read(timeout=100,timeout_key='-timeout-')

  if event == sg.WIN_CLOSED:
    print('exit')
    break

  if event.startswith('-t'): 
    comm.update()
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
  # update bit output widget
    val=comm.state.output_bit_registers0_to_31
    for n,k in enumerate(indices):
      if '-y'+k in window.AllKeysDict:
        window['-y'+k].update(background_color='yellow' if val&(1<<n) else 'black')
  # update sequence executer
    if thread is None:
      window['Stop'].update(button_color='black')
    else:
      window['Stop'].update(button_color='red' if thread.is_alive() else 'black')
    continue

  if event.startswith('-i'):
    print('reg',event[:4],values[event[:4]])
    exec('comm.inregs.input_int_register_'+event[2:]+'='+values[event[:4]])
    continue
  elif event.startswith('-x'):
    print('bit',event[:4],values[event[:4]])
    if values[event[:4]]:
      val=comm.inregs.input_bit_registers0_to_31 | (1<<int(event[2:]))
    else:
      val=comm.inregs.input_bit_registers0_to_31 & ~(1<<int(event[2:]))
    comm.inregs.input_bit_registers0_to_31=val
    continue

  if event.startswith('Seq'):
    do_sequence(event[8:])
    continue

  if event.startswith('Stop'):
    stop_sequence()
    continue

comm.pause()
comm.disconnect()
window.close()
if thread.is_alive():
  getOutBitRaiser=True

