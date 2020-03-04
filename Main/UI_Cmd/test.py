#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import  os  
import  sys
import  tty, termios
import time    

name_t='test2'
 
if name_t == 'test1':
    while True:
        fd=sys.stdin.fileno()
        old_settings=termios.tcgetattr(fd)
        #old_settings[3]= old_settings[3] & ~termios.ICANON & ~termios.ECHO  
        try:
            tty.setraw(fd)
            ch=sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
            #print 'error'
        print (ch)

def test2():
    print ('test2')
    from pynput.keyboard import Listener,Key
 
    input=''
    def press(key):
        nonlocal input
        try:
            print (key, type(key)) 
            input+=key.char
        except AttributeError:
            print (key, type(key))
            if key==Key.esc: print ('esc press')
            elif key==Key.enter: print ('enter press')
     
    listener= Listener(on_press = press)
    listener.start()
    while 1:
        time.sleep(2)
        print (input)
        
if name_t == 'test2': test2()
    