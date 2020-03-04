#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import  os  
import  sys
import  tty, termios
import time    
 
if __name__ == '__main__':

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

