#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
from Common import Config,Message
import socket,json

class Room:
    def __init__(self, socket_list):
        
        pass
    
    
    def send_recv(self, c_sock, msg):
        '''
        :向客户端发送包，等待回复
        '''
        c_sock.send(msg)
        try:
            tmsg=c_sock.recv(Config.BuffSize)
            if not tmsg: return False
            
        except  socket.timeout:
            print ('detected timeout')
            return False
        except:
            print ('unexpected error')
            return False
        return json.loads(tmsg)
    
    
    def start(self):
        pass
    
    

if __name__ == '__main__':
    pass