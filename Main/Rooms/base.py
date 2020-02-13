#coding:utf-8
'''
Created on 2020年2月12日

@author: sherl
'''
from Common import Config,Message
import socket,json

class Room_base:
    def __init__(self, socket_list):
        self.socket_list=socket_list
        
    
    
    def send_recv(self, c_sock, msg=None):
        '''
        :等待回复
        :若msg不为空则先发送msg
        '''
        if msg is not None: c_sock.send(msg)
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
    
    def send_recv_onebyone(self, sock_list, msg=None):
        ret=[]
        for i in sock_list:
            tep=self.send_recv(i, msg)
            if tep:
                ret.append(tep)
            else:
                ret.append(None)
        return ret
                
    def send_all(self, sock_list, msg):
        for i in sock_list:  i.send(msg)
            
    #游戏中用到的一些事件
    def on_gamestart(self):
        for ind, i in enumerate(self.socket_list):
            msg=Message.form_gamestart(ind, reply=False)
            i.send(msg)
            
    def on_gameend(self):
        msg=Message.form_gameend(reply=False)
        self.send_all(self.socket_list, msg)
    
    def on_pickhero(self):
        
        pass
    
    
    
    
    
    
    
    
    
    
    
    #main function
    def start(self):
        self.on_gamestart()
        
    
    










if __name__ == '__main__':
    pass











