#!/usr/bin/env python

import PySimpleGUI as sg
import sys
sys.path.append('.')

ids=[
  '0','1','2','3','4','5','6','7','8','9',
  '10','11','12','13','14','15','16','17','18','19',
  '20','21','22','23','24','25','26','27','28','29'
]
### Layout #####################
sg.theme('Dark Blue 3')
layout=[[
  sg.Text('Adds',size=(4,1)),
  sg.Text('Input',size=(10,1)),
  sg.Text('Output',size=(10,1)),
  sg.Text('X',size=(3,1)),
  sg.Text('Y',size=(3,1))
]]

for k in ids[:24]:   #Put widgets every one line
  ln=[
    sg.Text(k,size=(4,1)),
    sg.Input(key='-i'+k,size=(10,1)),
    sg.Input(key='-o'+k,size=(10,1),readonly=True),
    sg.Checkbox('',key='-x'+k),
    sg.Text('',key='-y'+k,size=(2,1),relief=sg.RELIEF_RIDGE,border_width=2,background_color='black')
  ]
  layout.append(ln)

# Put status widgets
layout.append([sg.Text('Robot mode',size=(12,1)),sg.Input(key='robot_mode',size=(10,1),readonly=True)])

### Render window #####################
window = sg.Window('I/O Monitor for UR', layout,finalize=True)
for k in ids[:24]:
  window['-i'+k].bind('<Return>', '')   #add event to the widget whose key is '-i*'
for k in ids[:24]:
  window['-x'+k].bind('<ButtonPress-1>', '')   #add event to the widget whose key is '-x*'

###Start RTDE comminucation################
import comm
IPADDS="127.0.0.1"
PORT=30004

if not comm.connect(IPADDS,PORT,"default.xml"):
  print("comm connect falied")
  sys.exit()

for k in ids[:24]:
  exec('comm.inregs.input_int_register_'+k+'=0')    #Init inregs(input registers)
  window['-i'+k].update(eval('comm.inregs.input_int_register_'+k))   #at the same time corresponding widget
comm.inregs.input_bit_registers0_to_31 = 0

if not comm.start():
  print("comm start falied")
  sys.exit()

while True:
  event, values = window.read(timeout=100,timeout_key='-timeout-')

  if event == sg.WIN_CLOSED:
    print('exit')
    break

  if event.startswith('-t'): 
    comm.update()
    window['robot_mode'].update(comm.state.robot_mode)
    continue

  if event.startswith('-i'):
    print('reg',event[:4],values[event[:4]])
    exec('comm.inregs.input_int_register_'+event[2:]+'='+values[event[:4]])
  elif event.startswith('-x'):
    print('bit',event[:4],values[event[:4]])
    if values[event[:4]]:
      val=comm.inregs.input_bit_registers0_to_31 | (1<<int(event[2:]))
    else:
      val=comm.inregs.input_bit_registers0_to_31 & ~(1<<int(event[2:]))
    comm.inregs.input_bit_registers0_to_31=val

comm.pause()
comm.disconnect()
window.close()

