#!/usr/bin/env python

#import sys
#sys.path.append("..")
import time
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config

inregs=None
con=None
state=None

def connect(host,port,xml):
  global con,inregs
  conf = rtde_config.ConfigFile(xml)
  state_names, state_types = conf.get_recipe("state")
  inregs_names, inregs_types = conf.get_recipe("input")

  try:
    con = rtde.RTDE(host,port)
    con.connect()
    print("connect...pass")

    con.get_controller_version()
    print("get version...pass")

    con.send_output_setup(state_names, state_types)
    inregs = con.send_input_setup(inregs_names, inregs_types)
    print("setup...pass")
  except Exception as e:
    print(e)
    return False
  else:
    return True

def start():   # start data synchronization
  if not con.send_start():
    print('send_start...failed')
    return False
  else:
    return True

def update():
  global state
  state = con.receive()
  if state is None:
    return None
  con.send(inregs)

def pause():
  con.send_pause()

def disconnect():
  con.disconnect()
