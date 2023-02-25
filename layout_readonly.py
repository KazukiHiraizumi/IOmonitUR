#!/usr/bin/env python
# Widgets should have keys as
#  Integer Input Verify"-v<address>"  e.g. "-v23"
#  Integer Output "-o<address>"  e.g. "-o23"
#  Bit Input Verify"-u<address>"  e.g. "-u23"
#  Bit Output "-y<address>"   e.g. "-y23"

import PySimpleGUI as sg

contents=None

def build(ids):
  global contents
  contents=[
    [ sg.Text('Robot mode'),
      sg.Input(key='robot_mode',size=(10,1),readonly=True),
      sg.Text('Runtime state'),
      sg.Input(key='runtime_state',size=(10,1),readonly=True) ],
    [ sg.Text('Adds',size=(4,1)),
      sg.Text('Input',size=(10,1)),
      sg.Text('Output',size=(10,1)),
      sg.Text('',size=(1,1)),
      sg.Text('X',size=(3,1)),
      sg.Text('',size=(1,1)),
      sg.Text('Y',size=(3,1)) ]
  ]

  for k in ids[:24]:   #Put widgets every one line
    ln=[
      sg.Text(k,size=(4,1)),
      sg.Input(key='-i'+k,size=(10,1),readonly=True),
      sg.Input(key='-o'+k,size=(10,1),readonly=True),
      sg.Text('',size=(1,1)),
      sg.Text('',key='-x'+k,size=(2,1),relief=sg.RELIEF_RIDGE,border_width=2,background_color='black'),
      sg.Text('',size=(1,1)),
      sg.Text('',key='-y'+k,size=(2,1),relief=sg.RELIEF_RIDGE,border_width=2,background_color='black')
    ]
    contents.append(ln)

  return contents

