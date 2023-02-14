#!/usr/bin/env python

import PySimpleGUI as sg
import sys
sys.path.append('.')

### Outlooking #####################
import layout_simple as layout
elements=[
  '0','1','2','3','4','5','6','7','8','9',
  '10','11','12','13','14','15','16','17','18','19',
  '20','21','22','23','24','25','26','27','28','29',
  '30','31','32','33','34','35','36','37','38','39',
  '40','41','42','43','44','45','46','47'
]
layout.build(elements)
window = sg.Window('I/O Monitor for UR', layout.layout,finalize=True)

for k in elements:
  if '-i'+k in window.AllKeysDict:
    window['-i'+k].bind('<Return>', '')   #attach event to the widget whose key is '-i*'
for k in elements:
  if '-x'+k in window.AllKeysDict:
    window['-x'+k].bind('<ButtonPress-1>', '')   #attach event to the widget whose key is '-x*'

###Start RTDE comminucation################
import comm
IPADDS="127.0.0.1"
PORT=30004
RECIPE="minimum.xml"

if not comm.connect(IPADDS,PORT,RECIPE):
  print("comm connect falied")
  sys.exit()

#Init inregs(input registers)
for k in elements:
  if '-i'+k in window.AllKeysDict:
    exec('comm.inregs.input_int_register_'+k+'=0')   #init int register
    window['-i'+k].update(eval('comm.inregs.input_int_register_'+k))   #ant its corresponding widget
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
    window['runtime_state'].update(comm.state.runtime_state)
  # update integer output widget
    for k in elements:
      try:
        val=eval('comm.state.output_int_register_'+k)
      except Exception as e:
        break
      if '-o'+k in window.AllKeysDict:
        window['-o'+k].update(val)
  # update bit output widget
    val=comm.state.output_bit_registers0_to_31
    for n,k in enumerate(elements):
      if '-y'+k in window.AllKeysDict:
        window['-y'+k].update(background_color='yellow' if val&(1<<n) else 'black')
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

