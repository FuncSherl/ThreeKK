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
 
    input_s=''
    goon=True
    def press(key):
        nonlocal input_s,goon
        try:
            print (key, type(key)) 
            input_s+=key.char
        except AttributeError:
            print (key, type(key))
            if key==Key.esc: 
                #sys.stdin.flush()
                goon=False
                return False
            elif key==Key.enter: 
                input()
                #sys.stdin.flush()
                print ('enter press')
     
    listener= Listener(on_press = press)
    listener.start()
    while goon:
        time.sleep(2)
        print (input_s)
        
if name_t == 'test2': test2()
    