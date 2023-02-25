#!/usr/bin/env python
# Widgets should have keys as
#  Integer Input "-i<address>"  e.g. "-i23"
#  Integer Output "-o<address>"  e.g. "-o23"
#  Integer Input Edit"-v<address>"  e.g. "-v23"
#  Bit Input "-x<address>"  e.g. "-x23"
#  Bit Output "-y<address>"   e.g. "-y23"
#  Bit Input Edit"-u<address>"  e.g. "-u23"

import PySimpleGUI as sg

contents=None

def build(ids):
  global contents
  contents=[
    [ sg.Text('Robot mode'),
      sg.Input(key='robot_mode',size=(10,1),readonly=True),
      sg.Text('Runtime state'),
      sg.Input(key='runtime_state',size=(10,1),readonly=True) ],
    [ sg.Text('Adds',size=(17,1)),
      sg.Text('Input',size=(14,1)),
      sg.Text('Output',size=(15,1)),
      sg.Text('X',size=(6,1)),
      sg.Text('Y',size=(3,1)) ]
  ]

  for k in ids[:24]:   #Put widgets every one line
    ln=[
      sg.Text(k,size=(4,1),justification='r'),
      sg.Input(key='-v'+k,size=(10,1),pad=0),
      sg.Text('▶',pad=0),
      sg.Input(key='-i'+k,size=(10,1),pad=0,readonly=True),
      sg.Text('',size=(1,1)),
      sg.Input(key='-o'+k,size=(10,1),readonly=True),
      sg.Text('',size=(1,1)),
      sg.Button(k,key='-u'+k,size=(2,1),font=('Ariel',5),pad=0),
#      sg.Checkbox('',key='-u'+k,size=(1,1)),
#      sg.Text('->'),
      sg.Text('',key='-x'+k,size=(2,1),relief=sg.RELIEF_RIDGE,border_width=2,background_color='black'),
      sg.Text('',size=(1,1)),
      sg.Text('',key='-y'+k,size=(2,1),relief=sg.RELIEF_RIDGE,border_width=2,background_color='black'),
    ]
    contents.append(ln)

  contents.append([
    sg.Button('Seq1',key='-s1'),
    sg.Button('Seq2',key='-s2'),
    sg.Button('Seq3',key='-s3'),
    sg.Button('Seq4',key='-s4'),
    sg.Button('Stop',key='-s0')
  ])

  return contents

